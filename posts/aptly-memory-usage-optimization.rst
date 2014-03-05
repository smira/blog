.. link:
.. description:
.. tags: aptly,go,golang,программирование
.. date: 2014/03/05 17:21:41
.. title: Оптимизация использования памяти в aptly
.. slug: aptly-memory-usage-optimization

В следующей версии (0.4) `aptly <http://www.aptly.info>`_ использование памяти в самых частых
операциях сократится в три раза благодаря несложным оптимизациям. Т.к. aptly написана на Go,
это будет короткая история об оптимизации использования памяти программами на Go.

Когда я начинал разрабатывать aptly, я подозревал, что использование памяти будет далеко не
оптимальным, т.к. aptly "переваривает" большое количество метаданных пакетов (например, зеркало
Debian репозитория может содержать информацию о 30 тыс. пакетов). Я не замечал, что aptly использует
много памяти до того, как не начал тестировать на виртуалке с 512 Мб памяти. aptly работала крайне
медленно из-за постоянного свопирования. Я такого никак не ожидал: почему используется столько памяти?

Для начала я применил тривиальные оптимизации:

* некоторые долгие операции (например, зеркалирование репозитория), происходят в рамках выполнения одной функции,
  и некоторые структуры данных становятся ненужными до окончания работы функции. Так, обнуляя (присваивая ``nil``) переменные,
  можено дать возможноть garbage collectorу освободить ненужную память до окончания выполнения функции.
* повторное использование буферов для сериализации структур (это безопасно, т.к. нет конкурентного доступа, а результат
  сериализации немедленно копируется).

Вместо того, чтобы создавать буфер каждый раз...

.. code-block:: go

    // Encode does msgpack encoding of Package
    func (p *Package) Encode() []byte {
        var buf bytes.Buffer

        encoder := codec.NewEncoder(&buf, &codec.MsgpackHandle{})
        encoder.Encode(p)

        return buf.Bytes()
    }

... можно использовать его повторно:

.. code-block:: go

    // Internal buffer reused by all Package.Encode operations
    var encodeBuf bytes.Buffer

    // Encode does msgpack encoding of Package, []byte should be copied, as buffer would
    // be used for the next call to Encode
    func (p *Package) Encode() []byte {
        encodeBuf.Reset()

        encoder := codec.NewEncoder(&encodeBuf, &codec.MsgpackHandle{})
        encoder.Encode(p)

        return encodeBuf.Bytes()
    }

Во-вторых, необходимо начать измерять то, что мы пытаемся оптимизировать: использование памяти. С помощью `поста в блоге CloudFlare <http://blog.cloudflare.com/recycling-memory-buffers-in-go>`_ это сделать совсем несложно. Вот что я обнаружил:

.. image:: /galleries/mem-verify0.png
    :alt: mem stats for aptly snapshot verify

.. image:: /galleries/mem-mirror-update1.png
    :alt: mem stats for aptly snapshot verify

.. TEASER_END

Первый график показывает использование памяти командой ``aptly snapshot verify``, которая проверяет удовлетворенность зависимостей
между пакетами в полном дистрибутиве Debian wheezy, а второй график -  команда ``aptly mirror update`` разбирает информацию о пакетах
и пытается построить пустую очередь загрузки.

Следующим шагом было `профилирование памяти и процессора <http://blog.golang.org/profiling-go-programs>`_, что привело
к следующим выводам:

* куча времени проводится внутри GC (неудивительно, при 800GB куче);
* все выделения памяти вполне ожидаемые, нет ничего "лишнего".

Больше всего памяти занимала структура ``Package``, которая представляет собой мета-информацию пакета, полученную из контрольных
файлов Debian. Некоторые части этой структуры были нужны всегда, а другие только в отдельных операциях. Так что основной
оптимизацией было разделение ``Package`` на отдельные куски, которые подгружаются из БД по мере необходимости, а затем
обнуляются.

Вот что получилось в конце:

.. image:: /galleries/mem-verify4.png
    :alt: mem stats for aptly snapshot verify

.. image:: /galleries/mem-mirror-update4.png
    :alt: mem stats for aptly snapshot verify

Как видно из этих графиков, garbage collector теперь освобождает гораздо больше памяти, а рост используемый памиятт стал
более линейным. Есть еще некоторое количество вещей, которое можно прооптимизировать, но я это сделаю в будущих версиях
aptly.

Чтобы получить такие графики, в aptly был добавлен код, который сбрасывает в файл содержимое структуры ``runtime.MemStats`` каждые 100 мс:

.. code-block:: go

    memstats := cmd.Flag.Lookup("memstats").Value.String()
    if memstats != "" {
        interval := cmd.Flag.Lookup("meminterval").Value.Get().(time.Duration)

        context.fileMemStats, err = os.Create(memstats)
        if err != nil {
            return err
        }

        context.fileMemStats.WriteString("# Time\tHeapSys\tHeapAlloc\tHeapIdle\tHeapReleased\n")

        go func() {
            var stats runtime.MemStats

            start := time.Now().UnixNano()

            for {
                runtime.ReadMemStats(&stats)
                if context.fileMemStats != nil {
                    context.fileMemStats.WriteString(fmt.Sprintf("%d\t%d\t%d\t%d\t%d\n",
                        (time.Now().UnixNano()-start)/1000000, stats.HeapSys, stats.HeapAlloc, stats.HeapIdle, stats.HeapReleased))
                    time.Sleep(interval)
                } else {
                    break
                }
            }
        }()
    }

Графики были отрисованы с помощью ``gnuplot`` и такого скрипта::

    set output 'mem.png'
    set term png
    set key box left
    set xlabel "Time (msec)"
    set ylabel "Mem (MB)"
    plot "mem.dat" using 1:($2/1e6) title 'HeapSys' with lines, "mem.dat" using 1:($3/1e6) title 'HeapAlloc' with lines, "mem.dat" using 1:($4/1e6) title 'HeapIdle' with lines
