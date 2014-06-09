.. title: aptly 0.6
.. slug: aptly-06
.. date: 2014/06/09 00:57:38
.. tags: aptly, devops
.. link:
.. description:
.. type: text


Новая версия `aptly <http://www.aptly.info>`_ 0.6 была выпущена 7-го июня. aptly можно скачать
в виде  `исполняемых файлов <http://www.aptly.info#download>`_ или подключив Debian-репозиторий::

    deb http://repo.aptly.info/ squeeze main

При установке из репозитория в первый раз, не забудьте проимпортировать ключ, которым подписан релиз::

    $ gpg --keyserver keys.gnupg.net --recv-keys 2A194991
    $ gpg -a --export 2A194991 | sudo apt-key add -

Вот самые важные новые возможности этой версии:

Публикация репозиториев из нескольких компонентов
-------------------------------------------------

Одной из основных идей aptly является список пакетов: snapshotы, зеркала и локальные репозитории -
это списки пакетов (если быть более точным, списки ссылок на пакетов). Когда происходит операции
слияния, перетаскивания, копирования или перемещения пакетов - пакеты перемещаются между списками.
Компоненты - это способ разбить список пакетов на группы, обычно эти группы имеют смысл только
для опубликованных репозиториев. В то же самое время сопоставление пакета и компонента
не является универсальным: Debian группирует пакеты в компоненты ``main``, ``contrib`` и ``non-free``,
Ubuntu использует другое разделение на компоненты, а сторонние репозитории используют компоненты
для разделения пакетов для разных версий Debian (например, ``squeeze``, ``wheezy`` и т.п.)  или для
обозначения стабильных и тестовый версий пакетов.

Чтобы не переусложнять aptly, я решил, что не стоит создавать отображение пакетов на компоненты и
не разбивать списки пакетов на компоненты. Каждый список (snapshot, зеркало или локальный репозиторий)
состоит из "одного компонента" (на самом деле в нем нет компонентов вообще). Во время публикация репозитория
несколько таких списков могут быть опубликованы как отдельные компоненты.

По умолчанию при создании зеркала aptly объединяет все компоненты в единый список. Если мы хотим
сохранить разделения, для каждого исходного комопонента необходимо создать зеркало::

    aptly mirror create wheezy-main http://ftp.ru.debian.org/debian/ wheezy main
    aptly mirror create wheezy-contrib http://ftp.ru.debian.org/debian/ wheezy main
    aptly mirror create wheezy-non-free http://ftp.ru.debian.org/debian/ wheezy non-free

    aptly mirror list -raw | xargs -n 1 aptly mirror update

Затем мы создадим snapshot для каждого зеркала::

    aptly snapshot create wheezy-main-7.5 from mirror wheezy-main
    aptly snapshot create wheezy-contrib-7.5 from mirror wheezy-contrib
    aptly snapshot create wheezy-non-free-7.5 from mirror wheezy-non-free

И опубликуем все snapshotы в едином репозитории, сохраняя исходную структуру компонентов
(мы публикуем distribution ``wheezy`` в префикс ``upstream``)::

    aptly publish snapshot -component=main,contrib,non-free wheezy upstream wheezy-main-7.5 wheezy-contrib-7.5 wheezy-non-free-7.5

aptly достаточно умен, чтобы самостоятельно определить имена компонентов, так что можно
опустить их имена (запятые необходимы, чтобы aptly знал количество компонентов)::

    aptly publish snapshot -component=,, wheezy upstream wheezy-main-7.5 wheezy-contrib-7.5 wheezy-non-free-7.5

Конечно, мы могли выполнять все обычные операции, которые поддерживает aptly: объединение snapshotов,
перетаскивание пакетов и т.п.


Обработка конфликтов пакетов
----------------------------

Пакет во вселенной пакетов Debian идентифицируется тройкой (architecture, name, version). Если у двух пакетов
одинаковые (architecture, name, version), но разное содержимое, такую ситуацию называют конфликтом
пакетов. Руководство Debian запрещение включение конфликтующих пакетов в репозитории, которые могут
использоваться совместно на одной машине (такие репозитории, которые могут быть включены в один файл
``apt.sources``). К сожалению, в действительности такие конфликты встречаются не так уж редко:
один такой пакет существует в репозиториях ``squeeze`` + security updates, другая такая же ситуация
в репозитории puppet, где собраны одни и те же версии пакетов для разных дистрибутивов Debian в одном
репозитории и разных компонентах.

До версии 0.6 при обнаружении конфликта aptly останавливался и не позволял продолжать операцию. В новой версии
aptly умеет обрабатывать такие конфликты, есть только одно ограничение: конфликт не должен произойти
в рамках одного списка (в одном snapshot, одном зеркале или локальном репозитории). Но это ограничение
вполне естественно, иначе конфликт может опубликован в одном репозитории, что точно недопустимо.

Это изменение незаметно для пользователей, обновившихся до версии 0.6: aptly в фоновом режиме по мере
обновления зеркал или создания новых snapshot обновляет способ хранения ссылок на пакеты.

Публикация пустых репозиториев
------------------------------

Многие люди используют aptly для автоматизации каких-то процессов, в том числе и с использованием
систем управления конфигурацией. Для таких сценариев использования удобно создать локальный
репозиторий (пустой), сразу его опубликовать, чтобы создать точку для ``apt.sources``, а потом
добавлять пакеты и обновлять опубликованный репозиторий.

До версии 0.6 aptly не позволял публиковать пустые репозитории, теперь это ограничение снято.
При публикации пустого репозитория необходимо сразу корректно задать список архитектур
(обычно aptly автоматически определяет список архитектур по списку пакетов, в случае пустого
списка это невозможно). После публикации изменить список архитектур уже неовзможно, для его
изменения потребуется удалить опубликованный репозиторий и опубликовать заново.

Объединение snapshotов: новая стратегия
---------------------------------------

aptly поддерживает слияние snapshotов - это может быть полезно для объединения основного репозитория
с обновлениями безопасности или со сторонним репозиторием. В версии 0.6 доступно три стратегии
объединения:

* из пакетов с одинаковой парой (architecture, name) остается тот, который принадлежит snapshotу, который
  расположен "правее" в командной строке (по умолчанию);
* из пакетов с одинаковой парой (architecture, name) остается тот, версия которого больше (``-latest``);
* все версии пакетов сохраняются (``-no-remove``, новое в 0.6).


Полный список изменений
-----------------------

Вот полный список изменений в версии 0.5:

.. raw:: html

  <ul>
    <li>support for multi-component published repositories (<a href="https://github.com/smira/aptly/issues/36">#36</a>)</li>
    <li>handling duplicate packages with different content gracefully (<a href="https://github.com/smira/aptly/issues/60">#60</a>)</li>
    <li>repositories published by aptly now can be consumed by debian-installer (<a href="https://github.com/smira/aptly/issues/61">#61</a>)</li>
    <li>new flag: <code>-no-remove</code> for <a href="http://www.aptly.info/#aptly-snapshot-merge">aptly snapshot merge</a> to merge snapshots with all package versions preserved (<a href="https://github.com/smira/aptly/issues/57">#57</a>)</li>
    <li>publishing of empty snapshots/repositories is possible (<a href="https://github.com/smira/aptly/issues/55">#55</a>)</li>
    <li><a href="http://www.aptly.info/#aptly-repo-add">aptly repo add</a> now exists with 1 if any of files failed to add (<a href="https://github.com/smira/aptly/issues/53">#53</a>)</li>
    <li>bug fix: <code>Package:</code> line comes first in package metadata (<a href="https://github.com/smira/aptly/issues/49">#49</a>)</li>
    <li>bug fix: when command parsing fails, aptly returns exit code 2 (<a href="https://github.com/smira/aptly/issues/52">#52</a>)</li>
    <li>bug fix: pulling more than 128 packates at once (<a href="https://github.com/smira/aptly/issues/53">#53</a>)</li>
    <li>bug fix: <a href="http://www.aptly.info/#aptly-graph">aptly graph</a> may get confused with package pull requests (<a href="https://github.com/smira/aptly/issues/58">#58</a>)</li>
  </ul>
