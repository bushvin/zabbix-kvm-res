zabbix-kvm-res
==============

KVM monitoring through Zabbix

Monitor your KVM resources through Zabbix

INSTALLATION
============
1. copy bin/zabbix-kvm-res.py to /usr/local/bin/
2. append zabbix_agentd.conf/UserParameters to /etc/zabbix_agentd.conf (or whatever location your zabbix_agentd.conf file is located at)
3. restart zabbix-agent daemon
4. import zbx_templates/zabbix_kvm.xml into your templates
5. apply template to kvm system
6. drink coffee and enjoy
