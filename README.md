zabbix-kvm-res
==============

libvirt monitoring through Zabbix

Monitor your libvirt resources through Zabbix


Dependencies
=============
- libvirt-python (tested with 4.5.0)
- zabbix 4.x

Installation
============
1. copy bin/zabbix-libvirt-res.py to /usr/local/bin/
2. copy zabbix_agentd.conf/libvirt.conf to /etc/zabbix/zabbix_agentd.d/
3. compile selinux module & import (as root)

```
    ]# cd selinux
    ]# /bin/rm -f zabbix_agent_libvirt.mod zabbix_agent_libvirt.pp
    ]# checkmodule -M -m -o zabbix_agent_libvirt.mod zabbix_agent_libvirt.te
    ]# semodule_package -o zabbix_agent_libvirt.pp -m zabbix_agent_libvirt.mod
    ]# semodule -i zabbix_agent_libvirt.pp
```
4. restart zabbix-agent daemon
5. import zbx_templates/zabbix_libvirt-4.xml into the Zabbix templates
6. apply template to libvirt system
7. drink coffee and enjoy

Acknowledgements
================
- [Patrik Uytterhoeven](https://github.com/Trikke76) for putting it out there
- [thirstycat](https://github.com/thirstycat) for helping out with the flags of some libvirt methods
- Stefano Blasco for providing feedback and code to make it work with libvirt-python 0.9.12.3)

