#!/usr/bin/env python2
import sys
from netaddr import IPNetwork

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Uso: %s <CIDR>\n" % sys.argv[0]
    else:
        for ip in IPNetwork(sys.argv[1]):
            print '%s' % ip
