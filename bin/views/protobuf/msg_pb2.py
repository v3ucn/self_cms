# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: msg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='msg.proto',
  package='msg',
  serialized_pb=_b('\n\tmsg.proto\x12\x03msg\"\xb0\x01\n\x03Msg\x12\x0e\n\x06msg_id\x18\x01 \x02(\t\x12\x10\n\x08msg_type\x18\x02 \x02(\x05\x12\r\n\x05title\x18\x03 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x02(\t\x12\x0e\n\x06ref_id\x18\x05 \x01(\t\x12\x10\n\x08ref_type\x18\x06 \x01(\x05\x12\x11\n\tref_title\x18\x07 \x01(\t\x12\x11\n\ttimestamp\x18\x08 \x01(\t\x12\x12\n\nactiontype\x18\t \x01(\x05\x12\x0b\n\x03url\x18\n \x01(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_MSG = _descriptor.Descriptor(
  name='Msg',
  full_name='msg.Msg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg_id', full_name='msg.Msg.msg_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg_type', full_name='msg.Msg.msg_type', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='title', full_name='msg.Msg.title', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='content', full_name='msg.Msg.content', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ref_id', full_name='msg.Msg.ref_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ref_type', full_name='msg.Msg.ref_type', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ref_title', full_name='msg.Msg.ref_title', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='msg.Msg.timestamp', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='actiontype', full_name='msg.Msg.actiontype', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='url', full_name='msg.Msg.url', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=195,
)

DESCRIPTOR.message_types_by_name['Msg'] = _MSG

Msg = _reflection.GeneratedProtocolMessageType('Msg', (_message.Message,), dict(
  DESCRIPTOR = _MSG,
  __module__ = 'msg_pb2'
  # @@protoc_insertion_point(class_scope:msg.Msg)
  ))
_sym_db.RegisterMessage(Msg)


# @@protoc_insertion_point(module_scope)