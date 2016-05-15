#!/usr/bin/env python2
from __future__ import print_function

import socket

import sys

from twisted.python.log import startLogging
from twisted.internet.protocol import DatagramProtocol, Factory
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor


class TcpDgram(Int32StringReceiver):
    def __init__(self, remoteDict):
        self.remoteDict = remoteDict

    def stringReceived(self, string):
        print(u"Got a message of {} bytes.".format(len(string)))

    def sendStringV(self, string):
        self.sendString(string)
        print(u"Sent a message of {} bytes.".format(len(string)))
        
class TcpFactory(Factory):
    def __init__(self):
        self.remoteDict = {} # maps remote addresses to mosh-server connection

    def buildProtocol(self, addr):
        return TcpDgram(self.remoteDict)


class UdpDgram(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        print(u"Got a datagram of {} bytes from {}:{}.".format(len(datagram), host, port))
        self.transport.write(
            datagram,
            (host, port))

    def sendDatagram(self, datagram, host, port):
        self.transport.write(
            datagram,
            (host, port))
        print(u"Sent a datagram of {} bytes to {}:{}.".format(len(datagram), host, port))

if __name__ == "__main__":

    startLogging(sys.stdout)

    proto = UdpDgram()
    protov6 = UdpDgram()
    # reactor.listenUDP(60001, proto)
    reactor.listenUDP(60001, protov6, interface="::")

    # reactor.listenTCP(60001, TcpFactory())
    reactor.listenTCP(60001, TcpFactory(), interface="::")

    reactor.run()
