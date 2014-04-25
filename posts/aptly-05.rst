.. title: aptly 0.5
.. slug: aptly-05
.. date: 2014/04/25 00:12:18
.. tags: aptly, devops
.. link:
.. description:
.. type: text

Новая версия `aptly <http://www.aptly.info>`_ 0.5 была выпущена сегодня. aptly можно скачать
в виде  `исполняемых файлов <http://www.aptly.info#download>`_ или подключив Debian-репозиторий::

    deb http://repo.aptly.info/ squeeze main

При установке из репозитория в первый раз, не забудьте проимпортировать ключ, которым подписан релиз::

    $ gpg --keyserver keys.gnupg.net --recv-keys 2A194991
    $ gpg -a --export 2A194991 | sudo apt-key add -

Вот самые важные новые возможности в этой версии:

Публикация локальных репозиториев
---------------------------------

Есть два основных случая использования локальных репозиториев:

* тестирование новых версий пакетов
* предоставление стабильного способа распространения новых версий

Во втором случае лучше всего создать snapshot локального репозитория и опубликовать его.
Однако когда активно тестируются новые версии, создание snapshot при каждом изменении выглядит
не очень разумным. aptly начиная с версии 0.5 поддерживает
`публикацию локальных репозиториев напрямую <http://www.aptly.info/#aptly-publish-repo>`_.
Более того, когда репозиторий обновляет, его опубликованное представление можно обновить в
`один шаг <http://www.aptly.info/#aptly-publish-update>`_.

При создании локального репозитория можно указать параметры, которые будут использоваться
по умолчанию при публикации  (distribution and component)::

    aptly repo create -distribution=wheezy testing-wheezy
    aptly repo add -remove-files testing-wheezy incoming/*.deb
    aptly publish repo testing-wheezy
    ...
    aptly repo add -remove-files testing-wheezy incoming/*.deb
    aptly publish update wheezy

.. TEASER_END

Переключение опубликованных snapshot
------------------------------------

Snapshot - это способ обеспечить повторяемость в наборе установленных пакетов, но
время от времени возникает необходимость обновить версии ПО или добавить новые
пакеты. Для публикации нового snapshot aptly до версии 0.5 требовала удалить старый
опубликованный snapshot, а затем опубликовать новый. Между этими действиями опубликованный
репозиторий не был работоспособен.

Теперь aptly поддерживает
`переключение опубликованных snapshotов <http://www.aptly.info/#aptly-publish-switch>`_.
aptly выполняет следующую последовательность действий, чтобы минимизировать время недоступности
репозитория:

* в первую очередь создаются ссылки на новые файлы пакетов;
* затем создаются файлы с метаданными (``Packages``, ``Release``, ...) с временными именами
* новые версии файлов метаданных замещают старые версии
* старые файлы пакетов вычищаются.

Например::

    aptly snapshot create wheezy-7.3 from mirror wheezy-main
    aptly publish snapshot wheezy-7.3
    ....
    aptly mirror update wheezy-main
    aptly snapshot create wheezy-7.4 from mirror wheezy-main
    aptly publish switch wheezy wheezy-7.4

Стратегия слияния
-----------------

При `слиянии snapshotов <http://www.aptly.info/#aptly-snapshot-merge>`_ aptly заменяет совпадающие
по имени и архитектуре пакеты в порядке следования их в командной строке. Это хорошо работает
при слиянии обычного репозитория и backportов. Но иногда такого недостаточно: например,
при слиянии обычного репозитория, updates и security. Теперь aptly поддерживает флаг ``-latest``,
который включает стратегию "выигрывает самая поздняя версия"::

    aptly snapshot merge -latest wheezy-latest wheezy-backports wheezy-main wheezy-security

Спасибо `Ryan Uber <https://github.com/ryanuber>`_ и `Keith Chambers <https://github.com/keithchambers>`_ за
идею и pull request.

Автоматизация
-------------

Иногда вам нужно сделать действия с целым набором зеркал, snapshotов и репозиториев. aptly с версии 0.5
поддерживает формат списка "raw", который легко распарсить. Например, обновим все зеркала Debian::

    aptly mirror list -raw | grep -E '^debian-.*' | xargs -n 1 aptly mirror update

Спасибо `Eric Keller <https://github.com/erickeller>`_ за идею.

Полный список изменений
-----------------------

Вот полный список изменений в версии 0.5:

.. raw:: html

    <ul>
        <li>Debian packages for aptly are <a href="http://www.aptly.info#download">available</a></li>
        <li>internal DB is compacted when calling <a href="http://www.aptly.info#aptly-db-cleanup">aptly db cleanup</a> (<a href="https://github.com/smira/aptly/issues/19">#19</a>)</li>
        <li>size is shown in human-readable format (<a href="https://github.com/smira/aptly/issues/18">#18</a>)</li>
        <li>fixed wrong location of man page in Debian package (<a href="https://github.com/smira/aptly/issues/22">#22</a>)</li>
        <li>new flags: <code>-distribution</code> and <code>-component</code> to specify default publishing options in <a href="http://www.aptly.info#aptly-repo-create">aptly repo create</a> (<a href="https://github.com/smira/aptly/issues/12">#12</a>)</li>
        <li>aptly would try harder to figure out distribution &amp; component automatically when publishing going through the tree of snapshots, mirrors and local repositories</li>
        <li>aptly supports publishing local repositories, without intermediate snapshot step (<a href="https://github.com/smira/aptly/issues/10">#10</a>)</li>
        <li>new command: <a href="http://www.aptly.info#aptly-publish-repo">aptly publish repo</a> to publish local repository directly (<a href="https://github.com/smira/aptly/issues/10">#10</a>)</li>
        <li>new command: <a href="http://www.aptly.info#aptly-repo-edit">aptly publish edit</a> to change defaults for the local repository (<a href="https://github.com/smira/aptly/issues/12">#12</a>)</li>
        <li>aptly supports global &amp; command flags placement in any position in command line (before command name, after command name) (<a href="https://github.com/smira/aptly/issues/17">#17</a>)</li>
        <li>new command: <a href="http://www.aptly.info#aptly-db-recover">aptly db recover</a> to recover internal DB after crash (<a href="https://github.com/smira/aptly/issues/25">#25</a>)</li>
        <li>new flag: <code>-raw</code> to display list in machine-readable format for commands <a href="http://www.aptly.info#aptly-mirror-list">aptly mirror list</a>, <a href="http://www.aptly.info#aptly-repo-list">aptly repo list</a>, <a href="http://www.aptly.info#aptly-snapshot-list">aptly snapshot list</a> and <a href="http://www.aptly.info#aptly-publish-list">aptly publish list</a> (<a href="https://github.com/smira/aptly/issues/27">#27</a>, <a href="https://github.com/smira/aptly/issues/31">#31</a>)</li>
        <li>new flags: <code>-origin</code> and <code>-label</code> to customize fields <code>Origin:</code> and <code>Label:</code> in <code>Release</code> files during publishing in commands <a href="http://www.aptly.info#aptly-publish-snapshot">aptly publish snapshot</a> and <a href="http://www.aptly.info#aptly-publish-repo">aptly publish repo</a> (<a href="https://github.com/smira/aptly/issues/29">#29</a>)</li>
        <li>bug fix: with some HTTP servers aptly might have given "size mismatch" errors due to unnecessary decompression (<a href="https://github.com/smira/aptly/issues/33">#33</a>)</li>
        <li>new command: <a href="http://www.aptly.info#aptly-publish-update">aptly publish update</a> updates published repo in-place (<a href="https://github.com/smira/aptly/issues/8">#8</a>)</li>
        <li>new command: <a href="http://www.aptly.info#aptly-publish-switch">aptly publish switch</a> switches published snapshot in-place (<a href="https://github.com/smira/aptly/issues/8">#8</a>)</li>
        <li>new flag: <code>-latest</code> for command <a href="http://www.aptly.info#aptly-snapshot-merge">aptly snapshot merge</a> changes merge strategy to "latest version wins" (<a href="https://github.com/smira/aptly/pull/42">#42</a>), thanks to <a href="https://github.com/ryanuber">@ryanuber</a> and <a href="https://github.com/keithchambers">@keithchambers</a></li>
    </ul>



