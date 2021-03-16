#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import json
from optparse import OptionParser
import argparse

try:
    import libvirt
except ModuleNotFoundError as e:
    print("Python module libvirt is most likely not installed, Please install python-libvirt", file=sys.stderr)
    sys.exit(1)

def main():
    args = parse_args()
    if args.resource == "pool":
        if args.action == "list":
            pool = Pool(uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = json.dumps(list_to_zbx(pool.list(), '{#POOLNAME}'), sort_keys=True, indent=2)
        elif args.action == "count_active":
            pool = Pool(uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = len(pool.list(active=True))
        elif args.action == "count_inactive":
            pool = Pool(uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = len(pool.list(active=False))
        elif args.action == "total":
            pool = Pool(args.pool,uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = pool.size['total']
        elif args.action == "used":
            pool = Pool(args.pool,uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = pool.size['used']
        elif args.action == "free":
            pool = Pool(args.pool,uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = pool.size['free']
        elif args.action == "active":
            pool = Pool(args.pool,uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = pool.isactive
        elif args.action == "UUID":
            pool = Pool(args.pool,uri=args.uri)
            is_none(pool.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = pool.uuid
        pool.disconnect()

    elif args.resource == "net":
        if args.action == "list":
            net = Net(uri=args.uri)
            is_none(net.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = json.dumps(list_to_zbx(net.list(), '{#NETNAME}'), sort_keys=True, indent=2)
        elif args.action == "count_active":
            net = Net(uri=args.uri)
            is_none(net.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = len(net.list(active=True))
        elif args.action == "count_inactive":
            net = Net(uri=args.uri)
            is_none(net.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = len(net.list(active=False))
        elif args.action == "active":
            net = Net(args.net,uri=args.uri)
            is_none(net.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = net.isactive
        elif args.action == "UUID":
            net = Net(args.net,uri=args.uri)
            is_none(net.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = net.uuid
        net.disconnect()

    elif args.resource == "domain":
        if args.action == "list":
            dom = Domain(uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = json.dumps(list_to_zbx(dom.list(), '{#DOMAINNAME}'), sort_keys=True, indent=2)
        elif args.action == "count_active":
            dom = Domain(uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = len(dom.list(active=True))
        elif args.action == "count_inactive":
            dom = Domain(uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = len(dom.list(active=False))
        elif args.action == "active":
            dom = Domain(args.domain,uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = dom.isactive
        elif args.action == "UUID":
            dom = Domain(args.domain,uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = dom.uuid
        elif args.action == 'vcpus_current':
            dom = Domain(args.domain,uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = dom.vcpus['current']
        elif args.action == 'vcpus_max':
            dom = Domain(args.domain,uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = dom.vcpus['max']
        elif args.action == 'memory_current':
            dom = Domain(args.domain,uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = dom.memory['current']
        elif args.action == 'memory_max':
            dom = Domain(args.domain,uri=args.uri)
            is_none(dom.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = dom.memory['max']
        dom.disconnect()

    elif args.resource == "host":
        if args.action == "version":
            host = Host(uri=args.uri)
            is_none(host.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = host.version
        elif args.action == "type":
            host = Host(uri=args.uri)
            is_none(host.conn,"Could not connect to KVM using '%s'." % args.uri, 2)
            r = host.type
        host.disconnect()
  
    print(r)

class Libvirt(object):
    def __init__(self, uri='qemu:///system'):
        self.uri = uri
        self.conn = None
        self.connect()
        if self.conn is not None and self.name is not None:
            self.get_info()

    def get_info(self):
        self.version = self.conn.getVersion()
        self.type = self.conn.getType()
        return None
    
    def connect(self, uri = None):
        if uri is None:
            uri = self.uri
        try:
            self.conn = libvirt.openReadOnly(uri)
        except:
            print("There was an error connecting to the local libvirt daemon using '%s'." % uri, file=sys.stderr)
            self.conn = None
        return self.conn

    def disconnect(self):
        return self.conn.close()

class Host(Libvirt):
    def __init__(self, uri='qemu:///system'):
        self.name = 'n/a'
        super(self.__class__, self).__init__(uri)

    def get_info(self):
        self.version = self.conn.getVersion()
        self.type = self.conn.getType()
        return None

class Domain(Libvirt):
    def __init__(self, domain=None, uri='qemu:///system'):
        self.name = domain
        super(self.__class__, self).__init__(uri)
    
    def get_info(self):
        self.domain = self.conn.lookupByName(self.name)
        self.isactive = self.domain.isActive()
        self.uuid = self.domain.UUIDString()
        if self.isactive:
            self.vcpus = { 'current': len(self.domain.vcpus()[0]),
                           'max': self.domain.maxVcpus() }
            self.memory = { 'current': self.domain.memoryStats()['actual'] *1024,
                            'max': self.domain.maxMemory() *1024 }
        else:
            self.vcpus = { 'current': 0,
                           'max': 0 }
            self.memory = { 'current': 0,
                            'max': 0 }
        return self.domain

    def list(self, active=None):
        self.domainlist = []
        try:
            if active is None:
                self.domainlist = [  d.name() for d in self.conn.listAllDomains(0) ]
            else:
                self.domainlist = [  d.name() for d in self.conn.listAllDomains(0) if d.isActive() == active ]
        except:
            print("Could not fetch list of domains.", file=sys.stderr)
            sys.exit(3)
        
        self.domainlist.sort()
        return self.domainlist

class Net(Libvirt):
    def __init__(self, net=None, uri='qemu:///system'):
        self.name = net
        super(self.__class__, self).__init__(uri)

    def get_info(self):
        self.net = self.conn.networkLookupByName(self.name)
        self.isactive = self.net.isActive()
        self.uuid = self.net.UUIDString()
        return self.net

    def list(self, active=None):
        self.netlist = []

        try:
            if active is None:
                self.netlist = [ n.name() for n in self.conn.listAllNetworks(0) ]
            else:
                self.netlist = [ n.name() for n in self.conn.listAllNetworks(0) if n.isActive() == active]

        except:
            print("Could not fetch list of networks.", file=sys.stderr)

        self.netlist.sort()
        return self.netlist

class Pool(Libvirt):
    def __init__(self, pool=None, uri='qemu:///system'):
        self.name = pool
        super(self.__class__, self).__init__(uri)
 
    def get_info(self):
        self.pool = self.conn.storagePoolLookupByName(self.name)
        self.size = { 'total': self.pool.info()[1],
                      'free': self.pool.info()[3],
                      'used': self.pool.info()[2]
                    }
        self.isactive = self.pool.isActive()
        self.uuid = self.pool.UUIDString()

    def list(self, active=None):
        self.poollist = []
        try:
            if active is None:
                self.poollist = [ p.name() for p in self.conn.listAllStoragePools(0) ]
            else:
                self.poollist = [ p.name() for p in self.conn.listAllStoragePools(0) if p.isActive() == active ]
        except:
            print("Could not fetch list of storage pools.", file=sys.stderr)
            sys.exit(3)

        self.poollist.sort()
        return self.poollist

def is_none(data, errormsg, rc):
    if data is None:
        print(errormsg, file=sys.stderr)
        sys.exit(rc)

def list_to_zbx(data, label):
    if not isinstance(data, (list,tuple)):
        return data

    r = dict(data=[])
    return { 'data': [ { label: e } for e in data ] }

def parse_args():
    valid_resource_types = [ "pool", "net", "domain", "host" ]
    pool_valid_actions = [ 'list', 'total', 'used', 'free', 'active', 'UUID', 'count_active', 'count_inactive' ]
    net_valid_actions = [ 'list', 'active', 'UUID', 'count_active', 'count_inactive' ]
    domain_valid_actions = [ 'list', 'active', 'UUID', 'vcpus_current', 'vcpus_max', 'memory_current', 'memory_max', 'count_active', 'count_inactive' ]
    host_valid_actions = [ "version", "type" ]

    parser = argparse.ArgumentParser(description='Return KVM information for Zabbix parsing')
    parser.add_argument('-U', '--uri', help="Connection URI", metavar='URI', type=str, default='qemu:///system')
    parser.add_argument('-R', '--resource', metavar='RESOURCE', dest='resource', help='Resource type to be queried', type=str, default=None)
    parser.add_argument('-A', '--action', metavar='ACTION', dest='action', help='The name of the action to be performed', type=str, default=None)
    parser.add_argument('-d', '--domain', metavar='DOMAIN', dest='domain', help='The name of the domain to be queried', type=str, default=None)
    parser.add_argument('-n', '--net', metavar='NET', dest='net', help='The name of the net to be queried', type=str, default=None)
    parser.add_argument('-p', '--pool', metavar='POOL', dest='pool', help='The name of the pool to be queried', type=str, default=None)
    
    args = parser.parse_args()
    if args.resource not in valid_resource_types:
        parser.error("The resource specified (%s) is not supported. Please select one of: %s." % (args.resource, ", ".join(valid_resource_types)))

    if args.resource == "pool":
        if args.action not in pool_valid_actions:
            parser.error("The specified storage pool action (%s) is not supported. Please select one of: %s." % (args.action, ", ".join(pool_valid_actions)))
    elif args.resource == "net":
        if args.action not in net_valid_actions:
            parser.error("The specified network action (%s) is not supported. Please select one of: %s." % (args.action,  ", ".join(net_valid_actions)))
    elif args.resource == "domain":
        if args.action not in domain_valid_actions:
            parser.error("The specified domain action (%s) is not supported. Please select one of: %s." % (args.action, ", ".join(domain_valid_actions)))
    elif args.resource == "host":
        if args.action not in host_valid_actions:
            parser.error("The specified host action (%s) is not supported. Please select one of: %s." % (args.action, ", ".join(host_valid_actions)))

    return args

if __name__ == "__main__":
    main()
