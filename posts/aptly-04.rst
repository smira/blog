.. link:
.. description:
.. tags: aptly, devops
.. date: 2014/03/11 16:14:03
.. title: aptly 0.4
.. slug: aptly-04

Сегодня вышла версия `aptly <http://www.aptly.info/>`_ 0.4: теперь aptly поддерживает работу с
`локальными репозиториями пакетов <http://www.aptly.info/#aptly-repo>`_. Теперь с помощью aptly можно
управлять коллекцией собственных пакетов, публиковать их, создавать snapshotы, объединять их с upstream
репозиториями.
`Скачивайте <http://www.aptly.info/#download>`_ или собирайте из `исходников <https://github.com/smira/aptly>`_,
`пишите багрепорты <https://github.com/smira/aplty/issues>`_, обсуждайте в
`группе aptly-discuss <https://groups.google.com/forum/#!forum/aptly-discuss>`_, читайте `меня (@smira) <https://twitter.com/smira/>`_
в Twitter, чтобы получить информацию о новых релизах.

К заметным нововведениям в версии 0.4 также можно отнести поддержку source пакетов, возможность удаления неиспользуемых
файлов, очистка базы данных и оптимизация объема используемой памяти.

Полный список изменений:

* поддержка локальных репозиториев пакетов
* aptly поддерживает зеркалирование и публикацию source-пакетов в дополнение к бинарным пакетам
* новая команда: ``aptly db cleanup`` убирает неиспользуемые файлы пакетов и записи в БД
* пиковое использование памяти было уменьшено в три раза
* новые параметры: ``-keyring`` и ``-secret-keyring`` в команде ``aptly snapshot publish``
* новый конфигурационный параметр: ``downloadSourcePackages`` включает зеркалирование source-пакетов
* новый параметр: ``-with-sources`` в команде ``aptly mirror create``
* новые параметры: ``dependencyFollowSource``  и ``-dep-follow-source``, позволяющие отслеживать``Source:`` зависимости
* новый команды в группе ``aptly repo``: ``add``, ``copy``, ``create``, ``drop``, ``import``, ``list``, ``move``, ``remove`` and ``show``
* команда ``aptly snapshot create`` поддерживает создание snapshot локальных репозиториев
* новый параметр `` -no-remove`` в команде ``aptly snapshot pull``: не удалять другие версии пакетов при перетаскивании
  (сохранять старые версии)
* команда ``aptly mirror create`` поддерживает сокращенные PPA url: ``ppa:user/project``
* новый конфигурационные параметры: ``ppaDistributorID`` и ``ppaCodename`` для указания правил обработки PPA url
* пакеты в списках печатаюся с подчеркиваниями вместо дефисов, например, ``pkg_1.3-3_amd64`` вместо ``pkg-1.3-3-amd64``

С возможностью работы с локальными репозиториями, схема сущностей aptly и связей между ними теперь выглядит так:

.. image:: /galleries/schema.png
    :alt: aptly schema