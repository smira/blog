Иногда необходимо забирать данные из БД MySQL в режиме реального времени во внешнюю систему, 
которая никак не связана с `MySQL <http://www.mysql.com/>`_. Существует множество возможных решений, например, 
можно реализовать "слейва" MySQL, который бы хранил полученные данные во внешней системе.


Одно из возможных решений - сделать "выгрузку" данных из MySQL с помощью 
`UDF (User Defined Functions) <http://dev.mysql.com/doc/refman/5.1/en/adding-functions.html>`_ и триггеров. Для этого необходимо 
поставить слейв MySQL, на котором уже повесить на интересующие таблицы триггеры, которые с помощью UDF будут выгружать поток 
изменений таблиц во внешнюю систему. Слейв необходим, т.к. если триггеры поставить на мастере, то в случае отката 
транзакции действия, уже сделанные триггерами, откатить не получится, а на слейв попадают только зафиксированные транзакции. 
Второе,чтобы триггеры работали на слейве, тип репликации должен быть выставлен на 
`STATEMENT-based </posts/20100215mysql-row-statement-mixed-replication-triggers.html>`_.


Порывшись в одном `интересном архиве <http://www.mysqludf.org/>`_ UDF для MySQL я нашел несколько функций, которые мне подошли:
 
* преобразование строки MySQL в json;
* интерфейс с memcached.

В результате получился следующий план действий: данные модифицируются на мастере, реплицируются на слейв с 
помощью STATEMENT-репликации. В процессе репликации на слейве запускаются триггеры, формируют с помощью UDF 
пакет обновлений в JSON, и передают его во внешнюю очередь (`memcacheq <http://memcachedb.org/memcacheq/>`_) по memcached-протоколу. 
Конечно, это не единственный возможный способ, но все UDF уже были почти готовы. После доделывания напильником 
UDF получился вполне стабильно работающий вариант.

Триггеры выглядят примерно следующим образом:

.. code:: sql

    CREATE FUNCTION kick_photos (row_id INT) RETURNS INT 
    BEGIN 
        SELECT memc_set('queue_db', (json_object('insert' AS action, 'photos' AS table_name, photos.id AS id, json_members('data', json_object(photos.user_id AS `user_id`,photos.width AS `width`,photos.created_at AS `created_at`,photos.filename AS `filename`,photos.parent_id AS `parent_id`,photos.content_type AS `content_type`,photos.height AS `height`,photos.thumbnail AS `thumbnail`,photos.size AS `size`))))) INTO @dummy FROM photos WHERE id = row_id; 
    RETURN @dummy; 
    END


    CREATE TRIGGER photos_INSERT AFTER INSERT ON photos FOR EACH ROW 
        SET @dummy = memc_set('queue_db', (json_object('insert' AS action, 'photos' AS table_name, NEW.id AS id, json_members('data', json_object(NEW.user_id AS `user_id`,NEW.parent_id AS `parent_id`,NEW.created_at AS `created_at`,NEW.filename AS `filename`,NEW.width AS `width`,NEW.content_type AS `content_type`,NEW.height AS `height`,NEW.thumbnail AS `thumbnail`,NEW.size AS `size`)))));


    CREATE TRIGGER photos_DELETE BEFORE DELETE ON photos FOR EACH ROW 
     SET @dummy = memc_set('queue_db', (json_object('delete' AS action, 'photos' AS table_name, OLD.id AS id, json_members('data', json_object(OLD.user_id AS `user_id`,OLD.parent_id AS `parent_id`,OLD.created_at AS `created_at`,OLD.filename AS `filename`,OLD.width AS `width`,OLD.content_type AS `content_type`,OLD.height AS `height`,OLD.thumbnail AS `thumbnail`,OLD.size AS `size`)))));


    CREATE TRIGGER photos_UPDATE AFTER UPDATE ON photos FOR EACH ROW 
    BEGIN 
        IF json_object(OLD.user_id AS `user_id`,OLD.parent_id AS `parent_id`,OLD.created_at AS `created_at`,OLD.filename AS `filename`,OLD.width AS `width`,OLD.content_type AS `content_type`,OLD.height AS `height`,OLD.thumbnail AS `thumbnail`,OLD.size AS `size`) <> json_object(NEW.user_id AS `user_id`,NEW.parent_id AS `parent_id`,NEW.created_at AS `created_at`,NEW.filename AS `filename`,NEW.width AS `width`,NEW.content_type AS `content_type`,NEW.height AS `height`,NEW.thumbnail AS `thumbnail`,NEW.size AS `size`) THEN 
            SET @dummy = memc_set('queue_db', (json_object('update' AS action, 'photos' AS table_name, OLD.id AS id, json_members('new', json_object(NEW.user_id AS `user_id`,NEW.parent_id AS `parent_id`,NEW.created_at AS `created_at`,NEW.filename AS `filename`,NEW.width AS `width`,NEW.content_type AS `content_type`,NEW.height AS `height`,NEW.thumbnail AS `thumbnail`,NEW.size AS `size`)), json_members('old', json_object(OLD.user_id AS `user_id`,OLD.parent_id AS `parent_id`,OLD.created_at AS `created_at`,OLD.filename AS `filename`,OLD.width AS `width`,OLD.content_type AS `content_type`,OLD.height AS `height`,OLD.thumbnail AS `thumbnail`,OLD.size AS `size`))))); 
        END IF; 
    END;


Комментарии:
 
* функция ``kick_photos`` позволяет скопировать строчку таблицы в очередь как пакет обновления типа "вставка", может 
  использоваться для начального наполнения внешней системы;
* триггеры на удаление и вставку просто формируют соответствующие пакеты;
* триггер на обновление проверяет, действительно ли в пакете произошли изменения (например, мы можем использовать не все поля в пакете); 
* необходимо учесть, что работе ``FOREIGN KEY CONSTRAINT`` триггеры не вызываются (очередной прикол MySQL), т.е., например, 
  если при выполнении запроса на удаление из таблицы ``A`` будут по ``FOREIGN KEY`` удалятся записи из таблицы ``B``, то в триггере 
  на удаление из ``A`` необходимо отработать этот случай, т.к. триггеры на таблице ``B`` не будут вызваны.


Код UDF доступен на github, это - "подпиленный" код из репозитория UDF или собственные разработки:


* `превращение строки в json <http://github.com/smira/lib_mysqludf_json>`_ - были грязно исправлены проблемы с buffer overrun;
* `запись в memcacheq <http://github.com/smira/memcached_functions_mysql>`_ - при запуске сервера будет настроена на запись в 
  ``localhost:22201``, плюс исправления для многопоточного режима и работы из нити workerа репликации;
* `timestamp с миллисекундной точностью <http://github.com/smira/mysql_udf_unix_timestamp_ms>`_ - полезно для проставления 
  временных меток и анализа производительности репликации.