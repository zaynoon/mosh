#!/usr/bin/env python2
from __future__ import print_function

import socket
import struct
import sys

from twisted.python.log import startLogging
from twisted.internet.protocol import DatagramProtocol, Factory
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor

import datagram_pb2


class ConnectionDatagram(Int32StringReceiver):
    def __init__(self, registry, remoteDict, connections):
        print(u"cd init")
        self.registry = registry
        self.remoteDict = remoteDict
        self.connections = connections

    def connectionMade(self):
        self.connections[self] = True

    def connectionLost(self, reason):
        del self.connections[self]

    def stringReceived(self, string):
        print(u"Got a message of {} bytes.".format(len(string)))
        datagram = datagram_pb2.Datagram()
        datagram.ParseFromString(string)
        family = datagram.remote.family
        host = socket.inet_ntop(socket.AF_INET6, datagram.remote.address[0])
        port = struct.unpack("!H", datagram.remote.address[1])[0]
        remote_addr = (family, datagram.remote.address[0], datagram.remote.address[1])
        print(u"Got family {}, host {} ({} bytes), port {}".
              format(family,
                     host, len(host),
                     port))
        self.remoteDict[remote_addr] = self
        self.registry[datagram_pb2.DatagramAddress.IPV6_UDP].sendDatagram(datagram.payload, host, port)

    def sendStringV(self, string):
        self.sendString(string)
        print(u"Sent a message of {} bytes.".format(len(string)))
        
class ConnectionFactory(Factory):
    def __init__(self, registry, remoteDict, connections):
        print(u"cf init")
        self.registry = registry # maps remote address families to datagram endpoints
        self.remoteDict = remoteDict # maps remote addresses to mosh-server connection
        self.connections = connections

    def buildProtocol(self, addr):
        return ConnectionDatagram(self.registry, self.remoteDict, self.connections)


class MessageDatagram(DatagramProtocol):
    def __init__(self, remoteDict, connections):
        print(u"md init")
        self.remoteDict = remoteDict
        self.connections = connections

    def datagramReceived(self, payload, (host, port)):
        print(u"Got a datagram of {} bytes from {}:{}.".format(len(payload), host, port))
        # self.transport.write(datagram,(host, port))
        datagram = datagram_pb2.Datagram()
        datagram.payload = payload
        family = datagram_pb2.DatagramAddress.IPV6_UDP
        host_packed = socket.inet_pton(socket.AF_INET6, host)
        port_packed = struct.pack("!H", port)
        
        datagram.remote.family = family
        datagram.remote.address.append(host_packed)
        datagram.remote.address.append(port_packed)
        remote_addr = (family, host_packed, port_packed)
        datagram_string = datagram.SerializeToString()
        if remote_addr in self.remoteDict:
            print(u"Sending direct")
            self.remoteDict[remote_addr].sendStringV(datagram_string)
        else:
            print(u"Sending everywhere")
            for remote in self.connections:
                print(u"sending")
                remote.sendStringV(datagram_string)

    def sendDatagram(self, datagram, host, port):
        self.transport.write(datagram,(host, port))
        print(u"Sent a datagram of {} bytes to {}:{}.".format(len(datagram), host, port))

if __name__ == "__main__":

    startLogging(sys.stdout)

    remoteDict = {}
    MessageRegistry = {}
    Connections = {}

    UDPEndpoint = MessageDatagram(remoteDict, Connections)
    UDPEndpointv6 = MessageDatagram(remoteDict, Connections)

    reactor.listenUDP(60001, UDPEndpoint)
    reactor.listenUDP(60001, UDPEndpointv6, interface="::")

    MessageRegistry[datagram_pb2.DatagramAddress.IPV4_UDP] = UDPEndpoint
    MessageRegistry[datagram_pb2.DatagramAddress.IPV6_UDP] = UDPEndpointv6
    
    reactor.listenTCP(60001, ConnectionFactory(MessageRegistry, remoteDict, Connections))
    reactor.listenTCP(60001, ConnectionFactory(MessageRegistry, remoteDict, Connections), interface="::")

    reactor.run()
