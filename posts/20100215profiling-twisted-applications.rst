.. image:: /galleries/kcachegrind.png

Часто сам забываю, как профилировать легко и быстро Twisted-приложения (с некоторым изменениями подойдет для любых Python-приложений). 
Кроме Twisted нам понадобится еще `KCachegrind <http://kcachegrind.sourceforge.net/>`_.


Запускаем наше приложение с включенным профайлингом:



.. code:: sh

    twistd -n --savestats --profile=myprog.hotshot myprog


Подаем нагрузку, профайл собирается. Теперь с помощью утилиты ``hotshot2cg`` из поставки KCachegrind превращаем 
hotshot-профайл в calltree-профайл, который уже умеет KCachegrind "кушать".


.. code:: sh

    hotshot2cg myprog.hotshot > myprog.calltree


Запускаем KCachegrind, открываем в нем полученный профайл:


.. code:: sh
    
    kcachegrind myprog.calltree

