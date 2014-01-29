.. link:
.. description:
.. tags: aptly, devops, meetup
.. date: 2014/01/29 12:24:00
.. title: aptly 0.2, Встреча DevOps Moscow январь 2013
.. slug: aptly-02-moscow-devops-meetup

Случилось два хороших события: вышла версия 0.2 `aptly <http://www.aptly.info>`_, и я представил aptly на
`январской встрече DevOps в Москве <http://tech.yandex.ru/events/yagosti/devops/>`_.

aptly - это система управления репозиториями пакетами Debian (в будущем и rpm-репозиториями), которая позволяет
контролировать то, какие версии пакетов будут установлены, а также изменять версии пакетов контролируемым образом.
Базовой концепцией aptly является snapshot - неизменяняемый срез репозитория пакетов, который обеспечивает
повторяемость. Операции над срезами позволяют, например, перетащить новую версию nginx из backports или
добавить к основному репозиторию пакет Percona MySQL Server из репозитория Percona.

К середине февраля должна выйти версия 0.3, в которой будут добавлены небольшие возможности, чтобы пользоваться
aptly было удобнее.

Пару слов про DevOps Meetup: огранизовано все было отлично, пришло очень много народу, интересные доклады.
`Следите <http://www.meetup.com/DevOps-Moscow-in-Russian/>`_ за следующими встречами! Видео моего доклада
про aptly `Яндекс уже выложил <http://tech.yandex.ru/events/yagosti/devops/talks/1598/>`_. Слайды
доклада можно скачать в формате `PDF </aptly_devops_meetup.pdf>`_ или посмотреть  в онлайне под катом.


.. TEASER_END

.. raw:: html

    <iframe src="http://www.slideshare.net/slideshow/embed_code/30566996" width="836" height="664" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>