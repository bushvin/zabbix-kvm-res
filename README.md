zabbix-kvm-res
==============

KVM monitoring through Zabbix

Monitor your KVM resources through Zabbix

Dependencies
=============
python2, libvirt-python (tested with 0.9.12.3, 0.10.2 and 1.1.3.x)

Installation
============
1. copy bin/zabbix-kvm-res.py to /usr/local/bin/
2. append zabbix_agentd.conf/UserParameters to /etc/zabbix_agentd.conf (or whatever location your zabbix_agentd.conf file is located at)
3. restart zabbix-agent daemon
4. import zbx_templates/zabbix_kvm.xml into your templates
5. apply template to kvm system
6. drink coffee and enjoy

Acknowledgements
================
- [Patrik Uytterhoeven](https://github.com/Trikke76) for putting it out there
- [thirstycat](https://github.com/thirstycat) for helping out with the flags of some libvirt methods
- Stefano Blasco for providing feedback and code to make it work with libvirt-python 0.9.12.3)
