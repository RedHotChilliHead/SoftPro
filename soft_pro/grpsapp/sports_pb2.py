# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sports.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csports.proto\x12\x06sports\"6\n\x12SportsLinesRequest\x12\x0e\n\x06sports\x18\x01 \x03(\t\x12\x10\n\x08interval\x18\x02 \x01(\x05\"z\n\x13SportsLinesResponse\x12\x35\n\x05lines\x18\x01 \x03(\x0b\x32&.sports.SportsLinesResponse.LinesEntry\x1a,\n\nLinesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\x32\x64\n\x0bSportsLines\x12U\n\x16SubscribeOnSportsLines\x12\x1a.sports.SportsLinesRequest\x1a\x1b.sports.SportsLinesResponse(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sports_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SPORTSLINESRESPONSE_LINESENTRY']._loaded_options = None
  _globals['_SPORTSLINESRESPONSE_LINESENTRY']._serialized_options = b'8\001'
  _globals['_SPORTSLINESREQUEST']._serialized_start=24
  _globals['_SPORTSLINESREQUEST']._serialized_end=78
  _globals['_SPORTSLINESRESPONSE']._serialized_start=80
  _globals['_SPORTSLINESRESPONSE']._serialized_end=202
  _globals['_SPORTSLINESRESPONSE_LINESENTRY']._serialized_start=158
  _globals['_SPORTSLINESRESPONSE_LINESENTRY']._serialized_end=202
  _globals['_SPORTSLINES']._serialized_start=204
  _globals['_SPORTSLINES']._serialized_end=304
# @@protoc_insertion_point(module_scope)
