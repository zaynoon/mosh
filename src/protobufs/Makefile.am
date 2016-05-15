source = userinput.proto hostinput.proto transportinstruction.proto datagram.proto

AM_CPPFLAGS = $(protobuf_CFLAGS)
AM_CXXFLAGS = $(WARNING_CXXFLAGS) $(HARDEN_CFLAGS) $(MISC_CXXFLAGS) -Wno-error

SUFFIXES = .proto .pb.cc .py

.proto.pb.cc:
	$(AM_V_GEN)$(PROTOC) --cpp_out=. -I$(srcdir) $<

datagram_pb2.py: datagram.proto
	$(AM_V_GEN)$(PROTOC) --python_out=. -I$(srcdir) datagram.proto

noinst_LIBRARIES = libmoshprotos.a

libmoshprotos_a_SOURCES = $(source)
nodist_libmoshprotos_a_SOURCES = $(source:.proto=.pb.cc) $(source:.proto=.pb.h)

BUILT_SOURCES = $(source:.proto=.pb.cc) datagram_pb2.py
CLEANFILES = $(source:.proto=.pb.cc) $(source:.proto=.pb.h) datagram_pb2.py
