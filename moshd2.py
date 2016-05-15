#!/usr/bin/env python2
from __future__ import print_function

import socket

import sys

from twisted.python.log import startLogging
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, DatagramProtocol

class SomeUDP(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        print(u"Got a datagram of {} bytes from {}:{}.".format(len(datagram), host, port))

    def sendFoo(self, foo, ip, port):
        self.transport.write(
            (u"Foo datagram: {}".format(foo)).encode("utf-8"),
            (ip, port))

class SomeSender(object):
    def __init__(self, proto):
        self.proto = proto

    def start(self, v4):
        self.v4 = v4
        reactor.callLater(3, self._send)

    def _send(self):
        if self.v4:
            self.proto.sendFoo(u"v4", b"127.0.0.1", 12345)
        else:
            self.proto.sendFoo(u"Hello or whatever", b"::1", 12345)
        self.start(self.v4)


if __name__ == "__main__":

    startLogging(sys.stdout)

    proto = SomeUDP()
    protov6 = SomeUDP()
    reactor.listenUDP(12345, proto)
    reactor.listenUDP(12345, protov6, interface="::")

    SomeSender(proto).start(True)
    SomeSender(protov6).start(False)

    reactor.run()
