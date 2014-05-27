distribute crontab
======================

最近一直在想怎么把单机上的任务分发到集群里面去执行， 当然有很多开源实现，如gearman等。
但是我是想用python来实现一个。

目前项目还在构想阶段，慢慢会放出架构和原理设计。

初步想的是读取配置文件的内容,后台的daemon程序定期执行:

* 配置文件(yaml)示例:

        connection: paramiko

        vars:
          url: http://www.hljyunxi.com

        jobs:
          - name: statistics
            pattern: all
            schedule: 'every 1 day'

            tasks:
              - name:
                action:

              - name:
                action

          - name: sample
            pattern: all
            just_one: True
            schedule: '2014-05-28 00:00:00'

            tasks:
              - name:
                action:

              - name:
                action

          - name: sample
            pattern: all
            just_one: True
            schedule: '2014-05-28 00:00:00'
            - include: sample.yml
