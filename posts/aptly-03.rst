.. link:
.. description:
.. tags: aptly, devops
.. date: 2014/02/10 23:20:40
.. title: aptly 0.3
.. slug: aptly-03

Сегодня вышла новая версия 0.3 `aptly <http://www.aptly.info/>`_. Это первая версия, которую я рекомендую для широкого
использования, `скачивайте <http://www.aptly.info/#download>`_ или собирайте из `исходников <https://github.com/smira/aptly>`_,
`пишите багрепорты <https://github.com/smira/aplty/issues>`_, обсуждайте в
`группе aptly-discuss <https://groups.google.com/forum/#!forum/aptly-discuss>`_, читайте `меня (@smira) <https://twitter.com/smira/>`_
в Twitter, чтобы получить информацию о новых релизах.

Новые возможности:

* с помощью команды `aptly serve <http://www.aptly.info/#aptly-serve>`_ можно быстро раздать по HTTP все опубликованные
  репозитории, aptly подскажет строчки для apt sources;
* при зеркалировании удаленных репозиториев aptly проверяет цифровую подпись и контрольные суммы загружаемых файлов, если в
  в вашей связке ключей GnuPG не хватает ключа для данного репозитория,
  aptly `подскажет <http://www.aptly.info/#aptly-mirror-create>`_ что делать;
* поддерживается flat-формат Debian-репозиториев (такие создает, например, `OBS <https://build.opensuse.org>`_);
* теперь можно удалять `зеркала (mirror) <http://www.aptly.info/#aptly-mirror-drop>`_ и
  `слепки (snapshot) <http://www.aptly.info/#aptly-snapshot-drop>`_;
* aptly может `визуализировать граф зависимостей <http://www.aptly.info/#aptly-graph>`_ между созданными зеркалами, слепками
  и опубликованными репозиториями;
* для aptly есть `bash completion <https://github.com/aptly-dev/aptly-bash-completion>`_, попробуйте, это очень удобно!
* aptly теперь умеет `создавать пустой слепок <http://www.aptly.info/#aptly-snapshot-create>`_ (snapshot);
* можно указать расположение конфигурационного файла с помощью ключа ``-config``.

Картинка для привлечения внимания (пример того, что может сделать `aptly graph <http://www.aptly.info/#aptly-graph>`_):

.. image:: /galleries/aptlygraph.png
    :alt: output of aptly graph command
