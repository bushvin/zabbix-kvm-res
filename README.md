zabbix-kvm-res
==============

KVM monitoring through Zabbix

Monitor your KVM resources through Zabbix

**Warning:** this has only been tested on Zabbix 1.8, 2.0 and 4.4

Dependencies
=============
python2, libvirt-python (tested with 0.9.12.3, 0.10.2, 1.1.3.x, 4.5.0)

Installation
============
1. copy bin/zabbix-kvm-res.py to /usr/local/bin/
1. Compile selinux module & import

```
    checkmodule -M -m -o zabbix_agent_libvirt.mod zabbix_agent_libvirt.te
    semodule_package -o zabbix_agent_libvirt.pp -m zabbix_agent_libvirt.mod
    semodule -i zabbix_agent_libvirt.pp
```
3. append zabbix_agentd.conf/UserParameters to /etc/zabbix_agentd.conf (or whatever location your zabbix_agentd.conf file is located at)
1. restart zabbix-agent daemon
1. import the appropriate modules from zbx_templates/ into your templates
1. apply template to kvm system
1. drink coffee and enjoy

Acknowledgements
================
- [Patrik Uytterhoeven](https://github.com/Trikke76) for putting it out there
- [thirstycat](https://github.com/thirstycat) for helping out with the flags of some libvirt methods
- Stefano Blasco for providing feedback and code to make it work with libvirt-python 0.9.12.3)

