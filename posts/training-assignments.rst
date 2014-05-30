.. title: Практические задания на мастер-классе
.. slug: training-assignments
.. date: 2014/05/30 01:05:41
.. tags: highload, разработка, рит
.. link:
.. description:
.. type: text

Первый `мастер-класс о высоких нагрузках и надежности <http://smira.highload.ru>`_ прошел успешно,
оказалось, что 900 слайдов на три дня даже слишком много :) В следующий раз
теоретическая часть будет немного покороче, а практики будет побольше. На мастер-классе было
`7 практических заданий </posts/highload-reliability-training-july.html>`_, каждое из которых
работало корректно у всех 25 участников на протяжении всех трех дней.
Я не ожидал, что не будет ни одной проблем.

Когда я начинал подготовку к мастер-классу, я понимал, что:

* задачи не должны зависеть от умения программировать: все знают разные языки программирования, да и сам
  процесс кодирования может занять много времени;
* потребуются различные сервисы в рамках заданий, установить их на ноутбуки участников и обеспечить
  отсутствие проблем будет сложно;
* я буду один на 25 человек, и подойти к каждому и помочь решить проблемы я не смогу.

Поэтому единственным вариантом оставалось подготовить сами задания (код) заранее и запускать их
в контролируемом окружении. Можно было выдать всем по образу виртуальной машины, но это опять-таки
потребует установки на все ноутбуки участников системы виртуализации, производительность каждой
машины будет разной. В результате я решил запустить виртуальные сервера в Amazon EC2, это имеет
следующие преимущества:

* одинаковое окружение у всех участников (как по составу, так и по производительности);
* участникам требуется только ssh;
* я могу централизовано управлять виртуальными машинами: готовить к следующему заданию и т.п.

.. TEASER_END

Минусы тоже есть:

* требуется надежный интернет (с этим как раз и были небольшие проблемы);
* эффективно редактировать код на удаленной машине могут лишь те, кто знает vim/emacs, остальным
  остается nano, в котором, правда, тяжеловато работать с кодом;
* виртуалки стоят денег, но это небольшая сумма по сравнению с другими расходами на мастер-класс.

Каждое задание я сначала готовил на своей машине, затем тестировал в будущей виртуалке, постепенно
меняя окружение. Идентичные виртуалки в Amazon проще всего поднять из одного готового образа, чтобы не
тратить время на настройку каждой машины. Для подготовки образа очень удобно использовать
`Packer <http://www.packer.io/>`_. Packer позволяет готовить образы виртуальных машин для разных окружений
от VirtualBox до облачных систем (в том числе и для Amazon EC2).

Для начала необходимо найти начальный образ операционной системы для использования в облаке, я делал на
базе Debian (`здесь можно найти нужный AMI <https://wiki.debian.org/Cloud/AmazonEC2Image/Wheezy>`_).
Нам нужен AMI в том регионе, в котором будем разворачивать виртуалки, вариант с паравиртуализацией
(он гораздо быстрее) и на базе EBS (можно и instance store, но там создавать образ гораздо сложнее).

После этого готовим файлы с инструкциями ``packer.json``:

.. code-block:: javascript

    {
      "variables": {
        "aws_access_key": "<ключ доступа>",
        "aws_secret_key": "<секретный ключ>"
      },
      "builders": [{
          "type": "amazon-ebs",
          "region": "us-east-1",
          "access_key": "{{user `aws_access_key`}}",
          "secret_key": "{{user `aws_secret_key`}}",
          "source_ami": "<который мы выбрали>",
          "instance_type": "m1.small",
          "ssh_username": "admin",

          "ssh_timeout": "5m",

          "ami_name": "teaching {{timestamp}}",

          "ami_block_device_mappings": [
              {
                  "device_name": "/dev/sdb",
                  "virtual_name": "ephemeral0"
              }
          ],

          "launch_block_device_mappings": [
              {
                  "device_name": "/dev/sdb",
                  "virtual_name": "ephemeral0"
              }
          ]
        },
        {
          "type": "virtualbox-ovf",
          "source_path": "wheezy.ovf",
          "ssh_username": "packer",
          "ssh_password": "packer",
          "ssh_wait_timeout": "30s",
          "shutdown_command": "sudo shutdown -h -P now"
        }
        ],
        "provisioners": [
            {
            "only": ["amazon-ebs"],
            "type": "shell",
            "execute_command": "{{ .Vars }} sudo -E sh '{{ .Path }}'",
            "inline": [
                "sed -i 's#,nobootwait##' /etc/fstab",
                "mount /mnt"
                    ]
            },
            {
            "type": "shell",
            "execute_command": "{{ .Vars }} sudo -E sh '{{ .Path }}'",
            "inline": [
                "apt-get update",
                "apt-get -y upgrade",
                "apt-get -y install memcached ...",
                "<дополнительные инструкции подготовки>",
                    ]
            }]
    }

Потребуются Access Key и Secret Key от Amazon, их можно создать с помощью IAM консоли. Лучше
создать отдельного пользователя для Packer и дать ему набор прав на управление EC2 и создание образов.

Секции ``"ami_block_device_mappings"`` и ``"launch_block_device_mappings"`` позволяют примонтировать
физический диск виртуальной машины (может быть полезно, если хочется исключить влияние сети). При этом
содержимое физического диска потеряется, конечно, при сбое виртуальной машины. В качестве размера
виртуалки можно выбрать ``m1.small``, она будет использоваться только для построения образа,
а такая будет дешевле. Готовый образ можно запускать на виртуалке большего размера.

Для построения виртуалки в VirtualBox потребуется подготовить образ ``wheezy.ovf``, который надо сделать
из такой же версии Debian, как и в AMI, плюс потребуется настроенный для ``sudo`` пользователь ``packer``
с доступом по паролю.

После этого запускаем Packer, который будет с таким файлом конфигурации строить одновременно образ
виртуалки в Amazon и локально в VirtualBox. Можно ограничить способы построения образов и сначала тестировать в VirtualBox,
а потом уже делать окончательный образ для Amazon.

Когда образ создан и протестирован, останется только запустить нужное количество виртуалок и управлять ими. Я использовал для
этого `thor <https://github.com/erikhuda/thor>`_ в качестве системы скриптования задач и `fog <http://fog.io/>`_ для
доступа в Amazon API.

Например, задача для создания виртуалки:

.. code-block:: ruby

    class Amazon < Thor
        def initialize(*args)
            super
            @ami_id = "ami-2ed23a46"
            @flavor_id = "m3.large"
            @servers = Fog::Compute.new(:provider => 'AWS', :region => 'us-east-1').servers
            @current_servers = @servers.select{|server| server.ready?}
        end

        desc "start", "start the cluster"
        method_options :number => 1
        def start
            options[:number].downto(1) do |n|

                puts "Creating server #{n}..."

                user = "student" + sprintf("%03d", rand(1000))

                server = @servers.bootstrap(:private_key_path => '~/.ssh/aws_teach_rsa',
                                            :public_key_path => '~/.ssh/aws_teach_rsa.pub',
                                            :username => 'admin',
                                            :flavor_id => @flavor_id,
                                            :image_id => @ami_id,
                                            :tags => {"Name" => user})

                server.wait_for{ print "."; ready? }

                passwd = `pwgen -1 10`.strip


                run_ssh_commands(server, "sudo useradd -m -p $(openssl passwd -1 #{passwd}) -s /bin/bash #{user}")
                run_ssh_commands(server, "sudo -i -u #{user} git clone https://github.com/smira/hl-tasks.git")

                puts
                puts "Server: #{server.public_ip_address}"
                puts "Login: #{user}"
                puts "Password: #{passwd}"
                puts
            end
        end
    end

P.S. Приходите на `мастер-класс 4-6 июля <http://smira.highload.ru/>`_, будет еще интереснее, чем в первый раз!
