#!/usr/bin/env python
from __future__ import print_function
import ConfigParser
import sys
import json
import httplib

FIELDS_REQUIRE = ('switch', 'active')
FIELDS_OPTIONAL = ('priority', 'actions')
FIELDS_12 = (
        'ingress-port', 'src-mac', 'dst-mac', 'vlan-id', 'vlan-priority',
        'ether-type', 'tos-bits', 'protocol',
        'src-ip', 'dst-ip', 'src-port', 'dst-port',
)

def log_err(msg):
    print('ERROR   : ' + msg)
    exit(1)

def log_warn(msg):
    print('WARNING : ' + msg)


def callapi(server, port, method, api, data):
    """ act like `curl -sX method -d data http://server:port/api`"""
    conn = httplib.HTTPConnection(server, port)
    conn.request(method, api, data)
    resp = conn.getresponse()
    return resp.read()


class StaticFlowPusher():
    def __init__(self, server, port):
        self.server, self.port = server, port

    def add_flow(self, entry):
        api = '/wm/staticflowentrypusher/json'
        ret = callapi(self.server, self.port, 'POST', api, json.dumps(entry))
        return json.loads(ret)

    def delete_flow(self, name):
        """delete one flow by name"""
        api = '/wm/staticflowentrypusher/json'
        data = {'name': name}
        ret = callapi(self.server, self.port, 'DELETE', api, json.dumps(data))
        return json.loads(ret)

    def clear_flow_all(self, switch='all'):
        """clear all flow on switch"""
        api = '/wm/staticflowentrypusher/clear/%s/json' % (switch,)
        ret = callapi(self.server, self.port, 'GET', api, '')
        return ret      # ret == ''
        #return json.loads(ret)

    def list_flow(self, switch='all'):
        api = '/wm/staticflowentrypusher/list/%s/json' % (switch,)
        ret = callapi(self.server, self.port, 'GET', api, '')
        return json.loads(ret)


def parse_config(filename):
    config = ConfigParser.ConfigParser()
    config.read(filename)

    # check all fields and no-use field
    if not config.has_section('controller'):
        log_err('You should have [controller] in config file.')

    if not config.has_option('controller', 'server'):
        log_err('You should have server in [controller]')

    if not config.has_option('controller', 'port'):
        log_err('You should have port in [controller]')

    # collect data
    ret = {}
    ret['server'] = config.get('controller', 'server')
    ret['port'] = config.get('controller', 'port')
    ret['entries'] = []

    for name in config.sections():
        if name == 'controller': continue

        # check omitted options
        for option in config.options(name):
            if option not in FIELDS_REQUIRE + FIELDS_OPTIONAL + FIELDS_12:
                log_warn('[%s] %s: omitted' % (name, option))

        entry = {'name': name}

        for field in FIELDS_REQUIRE:
            if not config.has_option(name, field):
                log_err('[%s] %s is required.' % (name , field))
            entry[field] = config.get(name, field)

        for field in FIELDS_OPTIONAL + FIELDS_12:
            if config.has_option(name, field):
                entry[field] = config.get(name, field)

        ret['entries'].append(entry)

    print('%d entries is loaded.' % (len(ret['entries'])))
    print([entry['name'] for entry in ret['entries']])
    return ret


def main(action, config_file):
    config = parse_config(config_file)

    pusher = StaticFlowPusher(config['server'], config['port'])
    
    if action == 'add':
        pusher.clear_flow_all()
        for entry in config['entries']:
            print(pusher.add_flow(entry))
    
    elif action == 'clear':
        pusher.clear_flow_all()
        
    elif action == 'show':
        print(json.dumps(pusher.list_flow(), indent=4))
    
    else:
        log_warn('Unknown Error')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage: %s (add|clear|show) config_file' % (sys.argv[0]))
        exit(1)
    
    main(sys.argv[1], sys.argv[2])

