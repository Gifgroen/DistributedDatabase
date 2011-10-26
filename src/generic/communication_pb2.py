# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='communication.proto',
  package='',
  serialized_pb='\n\x13\x63ommunication.proto\"\x99\x01\n\x13HashedStorageHeader\x12\x39\n\rhashAlgorithm\x18\x01 \x02(\x0e\x32\".HashedStorageHeader.HashAlgorithm\x12\x0c\n\x04hash\x18\x02 \x02(\x0c\x12\x1e\n\x06header\x18\x03 \x02(\x0b\x32\x0e.StorageHeader\"\x19\n\rHashAlgorithm\x12\x08\n\x04SHA1\x10\x01\"\xa7\x01\n\rStorageHeader\x12+\n\toperation\x18\x01 \x02(\x0e\x32\x18.StorageHeader.Operation\x12\x0e\n\x06offset\x18\x02 \x02(\x04\x12\x0e\n\x06length\x18\x03 \x02(\x04\x12\x18\n\x10requestTimestamp\x18\x04 \x02(\x04\"/\n\tOperation\x12\x08\n\x04READ\x10\x01\x12\t\n\x05WRITE\x10\x02\x12\r\n\tXOR_WRITE\x10\x03\"\x95\x01\n\x15StorageResponseHeader\x12-\n\x06status\x18\x01 \x02(\x0e\x32\x1d.StorageResponseHeader.Status\x12\x1e\n\x06header\x18\x02 \x02(\x0b\x32\x0e.StorageHeader\x12\x10\n\x08\x65rrorMsg\x18\x03 \x01(\t\"\x1b\n\x06Status\x12\x06\n\x02OK\x10\x01\x12\t\n\x05\x45RROR\x10\x02\"\xb6\x01\n\x18\x44ictionaryResponseHeader\x12\x30\n\x06status\x18\x01 \x02(\x0e\x32 .DictionaryResponseHeader.Status\x12 \n\tlocations\x18\x02 \x03(\x0b\x32\r.DataLocation\x12\x0b\n\x03key\x18\x03 \x01(\t\"9\n\x06Status\x12\x06\n\x02OK\x10\x01\x12\x11\n\rNO_FREE_SPACE\x10\x02\x12\x14\n\x10NOT_EXISTING_KEY\x10\x03\"P\n\x0c\x44\x61taLocation\x12$\n\x06header\x18\x01 \x02(\x0b\x32\x14.HashedStorageHeader\x12\x0c\n\x04port\x18\x02 \x02(\x04\x12\x0c\n\x04host\x18\x03 \x02(\t\"\x97\x01\n\x10\x44ictionaryHeader\x12.\n\toperation\x18\x01 \x02(\x0e\x32\x1b.DictionaryHeader.Operation\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\x0c\n\x04size\x18\x03 \x01(\x04\"8\n\tOperation\x12\x07\n\x03GET\x10\x01\x12\x07\n\x03\x41\x44\x44\x10\x02\x12\n\n\x06\x44\x45LETE\x10\x03\x12\r\n\tHEARTBEAT\x10\x04\"\xa2\x01\n\x1cStorageAdminRequestContainer\x12:\n\toperation\x18\x01 \x02(\x0e\x32\'.StorageAdminRequestContainer.Operation\x12\x13\n\x0bmessageData\x18\x02 \x01(\x0c\"1\n\tOperation\x12\x12\n\x0eSET_XOR_SERVER\x10\x01\x12\x10\n\x0cRECOVER_FROM\x10\x02\"8\n\x1aStorageAdminServerLocation\x12\x0c\n\x04host\x18\x01 \x02(\t\x12\x0c\n\x04port\x18\x02 \x02(\x04\"{\n\x1dStorageAdminRecoveryOperation\x12,\n\x07serverA\x18\x01 \x02(\x0b\x32\x1b.StorageAdminServerLocation\x12,\n\x07serverB\x18\x02 \x02(\x0b\x32\x1b.StorageAdminServerLocation\"s\n\x14StorageAdminResponse\x12,\n\x06status\x18\x01 \x02(\x0e\x32\x1c.StorageAdminResponse.Status\x12\x10\n\x08\x65rrorMsg\x18\x02 \x01(\t\"\x1b\n\x06Status\x12\x06\n\x02OK\x10\x01\x12\t\n\x05\x45RROR\x10\x02\"e\n\rAdminResponse\x12%\n\x06status\x18\x01 \x02(\x0e\x32\x15.AdminResponse.Status\x12\x10\n\x08\x65rrorMsg\x18\x02 \x01(\t\"\x1b\n\x06Status\x12\x06\n\x02OK\x10\x01\x12\t\n\x05\x45RROR\x10\x02\"@\n\x0e\x44ictionaryKeys\x12\x0c\n\x04keys\x18\x01 \x03(\t\x12 \n\x08response\x18\x02 \x02(\x0b\x32\x0e.AdminResponse\"\xa9\x01\n\x10RequestContainer\x12\x34\n\x0cnotification\x18\x01 \x02(\x0e\x32\x1e.RequestContainer.Notification\x12\x13\n\x0bmessageData\x18\x02 \x01(\x0c\"J\n\x0cNotification\x12\r\n\tNEW_SLAVE\x10\x01\x12\x0e\n\nNEW_MASTER\x10\x02\x12\r\n\tIS_MASTER\x10\x03\x12\x0c\n\x08IS_SLAVE\x10\x04\"0\n\x12\x44ictionaryLocation\x12\x0c\n\x04host\x18\x02 \x02(\t\x12\x0c\n\x04port\x18\x03 \x02(\x04\x42\x02H\x03')



_HASHEDSTORAGEHEADER_HASHALGORITHM = descriptor.EnumDescriptor(
  name='HashAlgorithm',
  full_name='HashedStorageHeader.HashAlgorithm',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='SHA1', index=0, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=152,
  serialized_end=177,
)

_STORAGEHEADER_OPERATION = descriptor.EnumDescriptor(
  name='Operation',
  full_name='StorageHeader.Operation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='READ', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='WRITE', index=1, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='XOR_WRITE', index=2, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=300,
  serialized_end=347,
)

_STORAGERESPONSEHEADER_STATUS = descriptor.EnumDescriptor(
  name='Status',
  full_name='StorageResponseHeader.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='OK', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=472,
  serialized_end=499,
)

_DICTIONARYRESPONSEHEADER_STATUS = descriptor.EnumDescriptor(
  name='Status',
  full_name='DictionaryResponseHeader.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='OK', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='NO_FREE_SPACE', index=1, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='NOT_EXISTING_KEY', index=2, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=627,
  serialized_end=684,
)

_DICTIONARYHEADER_OPERATION = descriptor.EnumDescriptor(
  name='Operation',
  full_name='DictionaryHeader.Operation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='GET', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ADD', index=1, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='DELETE', index=2, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='HEARTBEAT', index=3, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=864,
  serialized_end=920,
)

_STORAGEADMINREQUESTCONTAINER_OPERATION = descriptor.EnumDescriptor(
  name='Operation',
  full_name='StorageAdminRequestContainer.Operation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='SET_XOR_SERVER', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='RECOVER_FROM', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1036,
  serialized_end=1085,
)

_STORAGEADMINRESPONSE_STATUS = descriptor.EnumDescriptor(
  name='Status',
  full_name='StorageAdminResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='OK', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=472,
  serialized_end=499,
)

_ADMINRESPONSE_STATUS = descriptor.EnumDescriptor(
  name='Status',
  full_name='AdminResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='OK', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=472,
  serialized_end=499,
)

_REQUESTCONTAINER_NOTIFICATION = descriptor.EnumDescriptor(
  name='Notification',
  full_name='RequestContainer.Notification',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='NEW_SLAVE', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='NEW_MASTER', index=1, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='IS_MASTER', index=2, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='IS_SLAVE', index=3, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1652,
  serialized_end=1726,
)


_HASHEDSTORAGEHEADER = descriptor.Descriptor(
  name='HashedStorageHeader',
  full_name='HashedStorageHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='hashAlgorithm', full_name='HashedStorageHeader.hashAlgorithm', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hash', full_name='HashedStorageHeader.hash', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='header', full_name='HashedStorageHeader.header', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HASHEDSTORAGEHEADER_HASHALGORITHM,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=24,
  serialized_end=177,
)


_STORAGEHEADER = descriptor.Descriptor(
  name='StorageHeader',
  full_name='StorageHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='operation', full_name='StorageHeader.operation', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='offset', full_name='StorageHeader.offset', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='length', full_name='StorageHeader.length', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='requestTimestamp', full_name='StorageHeader.requestTimestamp', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STORAGEHEADER_OPERATION,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=180,
  serialized_end=347,
)


_STORAGERESPONSEHEADER = descriptor.Descriptor(
  name='StorageResponseHeader',
  full_name='StorageResponseHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='StorageResponseHeader.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='header', full_name='StorageResponseHeader.header', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='errorMsg', full_name='StorageResponseHeader.errorMsg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STORAGERESPONSEHEADER_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=350,
  serialized_end=499,
)


_DICTIONARYRESPONSEHEADER = descriptor.Descriptor(
  name='DictionaryResponseHeader',
  full_name='DictionaryResponseHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='DictionaryResponseHeader.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='locations', full_name='DictionaryResponseHeader.locations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='DictionaryResponseHeader.key', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DICTIONARYRESPONSEHEADER_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=502,
  serialized_end=684,
)


_DATALOCATION = descriptor.Descriptor(
  name='DataLocation',
  full_name='DataLocation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='header', full_name='DataLocation.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='port', full_name='DataLocation.port', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='host', full_name='DataLocation.host', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
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
  serialized_start=686,
  serialized_end=766,
)


_DICTIONARYHEADER = descriptor.Descriptor(
  name='DictionaryHeader',
  full_name='DictionaryHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='operation', full_name='DictionaryHeader.operation', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='key', full_name='DictionaryHeader.key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='size', full_name='DictionaryHeader.size', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DICTIONARYHEADER_OPERATION,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=769,
  serialized_end=920,
)


_STORAGEADMINREQUESTCONTAINER = descriptor.Descriptor(
  name='StorageAdminRequestContainer',
  full_name='StorageAdminRequestContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='operation', full_name='StorageAdminRequestContainer.operation', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='messageData', full_name='StorageAdminRequestContainer.messageData', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STORAGEADMINREQUESTCONTAINER_OPERATION,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=923,
  serialized_end=1085,
)


_STORAGEADMINSERVERLOCATION = descriptor.Descriptor(
  name='StorageAdminServerLocation',
  full_name='StorageAdminServerLocation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='host', full_name='StorageAdminServerLocation.host', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='port', full_name='StorageAdminServerLocation.port', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=1087,
  serialized_end=1143,
)


_STORAGEADMINRECOVERYOPERATION = descriptor.Descriptor(
  name='StorageAdminRecoveryOperation',
  full_name='StorageAdminRecoveryOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='serverA', full_name='StorageAdminRecoveryOperation.serverA', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='serverB', full_name='StorageAdminRecoveryOperation.serverB', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=1145,
  serialized_end=1268,
)


_STORAGEADMINRESPONSE = descriptor.Descriptor(
  name='StorageAdminResponse',
  full_name='StorageAdminResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='StorageAdminResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='errorMsg', full_name='StorageAdminResponse.errorMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STORAGEADMINRESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1270,
  serialized_end=1385,
)


_ADMINRESPONSE = descriptor.Descriptor(
  name='AdminResponse',
  full_name='AdminResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='AdminResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='errorMsg', full_name='AdminResponse.errorMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADMINRESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1387,
  serialized_end=1488,
)


_DICTIONARYKEYS = descriptor.Descriptor(
  name='DictionaryKeys',
  full_name='DictionaryKeys',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='keys', full_name='DictionaryKeys.keys', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='response', full_name='DictionaryKeys.response', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=1490,
  serialized_end=1554,
)


_REQUESTCONTAINER = descriptor.Descriptor(
  name='RequestContainer',
  full_name='RequestContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='notification', full_name='RequestContainer.notification', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='messageData', full_name='RequestContainer.messageData', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REQUESTCONTAINER_NOTIFICATION,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1557,
  serialized_end=1726,
)


_DICTIONARYLOCATION = descriptor.Descriptor(
  name='DictionaryLocation',
  full_name='DictionaryLocation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='host', full_name='DictionaryLocation.host', index=0,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='port', full_name='DictionaryLocation.port', index=1,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=1728,
  serialized_end=1776,
)

_HASHEDSTORAGEHEADER.fields_by_name['hashAlgorithm'].enum_type = _HASHEDSTORAGEHEADER_HASHALGORITHM
_HASHEDSTORAGEHEADER.fields_by_name['header'].message_type = _STORAGEHEADER
_HASHEDSTORAGEHEADER_HASHALGORITHM.containing_type = _HASHEDSTORAGEHEADER;
_STORAGEHEADER.fields_by_name['operation'].enum_type = _STORAGEHEADER_OPERATION
_STORAGEHEADER_OPERATION.containing_type = _STORAGEHEADER;
_STORAGERESPONSEHEADER.fields_by_name['status'].enum_type = _STORAGERESPONSEHEADER_STATUS
_STORAGERESPONSEHEADER.fields_by_name['header'].message_type = _STORAGEHEADER
_STORAGERESPONSEHEADER_STATUS.containing_type = _STORAGERESPONSEHEADER;
_DICTIONARYRESPONSEHEADER.fields_by_name['status'].enum_type = _DICTIONARYRESPONSEHEADER_STATUS
_DICTIONARYRESPONSEHEADER.fields_by_name['locations'].message_type = _DATALOCATION
_DICTIONARYRESPONSEHEADER_STATUS.containing_type = _DICTIONARYRESPONSEHEADER;
_DATALOCATION.fields_by_name['header'].message_type = _HASHEDSTORAGEHEADER
_DICTIONARYHEADER.fields_by_name['operation'].enum_type = _DICTIONARYHEADER_OPERATION
_DICTIONARYHEADER_OPERATION.containing_type = _DICTIONARYHEADER;
_STORAGEADMINREQUESTCONTAINER.fields_by_name['operation'].enum_type = _STORAGEADMINREQUESTCONTAINER_OPERATION
_STORAGEADMINREQUESTCONTAINER_OPERATION.containing_type = _STORAGEADMINREQUESTCONTAINER;
_STORAGEADMINRECOVERYOPERATION.fields_by_name['serverA'].message_type = _STORAGEADMINSERVERLOCATION
_STORAGEADMINRECOVERYOPERATION.fields_by_name['serverB'].message_type = _STORAGEADMINSERVERLOCATION
_STORAGEADMINRESPONSE.fields_by_name['status'].enum_type = _STORAGEADMINRESPONSE_STATUS
_STORAGEADMINRESPONSE_STATUS.containing_type = _STORAGEADMINRESPONSE;
_ADMINRESPONSE.fields_by_name['status'].enum_type = _ADMINRESPONSE_STATUS
_ADMINRESPONSE_STATUS.containing_type = _ADMINRESPONSE;
_DICTIONARYKEYS.fields_by_name['response'].message_type = _ADMINRESPONSE
_REQUESTCONTAINER.fields_by_name['notification'].enum_type = _REQUESTCONTAINER_NOTIFICATION
_REQUESTCONTAINER_NOTIFICATION.containing_type = _REQUESTCONTAINER;
DESCRIPTOR.message_types_by_name['HashedStorageHeader'] = _HASHEDSTORAGEHEADER
DESCRIPTOR.message_types_by_name['StorageHeader'] = _STORAGEHEADER
DESCRIPTOR.message_types_by_name['StorageResponseHeader'] = _STORAGERESPONSEHEADER
DESCRIPTOR.message_types_by_name['DictionaryResponseHeader'] = _DICTIONARYRESPONSEHEADER
DESCRIPTOR.message_types_by_name['DataLocation'] = _DATALOCATION
DESCRIPTOR.message_types_by_name['DictionaryHeader'] = _DICTIONARYHEADER
DESCRIPTOR.message_types_by_name['StorageAdminRequestContainer'] = _STORAGEADMINREQUESTCONTAINER
DESCRIPTOR.message_types_by_name['StorageAdminServerLocation'] = _STORAGEADMINSERVERLOCATION
DESCRIPTOR.message_types_by_name['StorageAdminRecoveryOperation'] = _STORAGEADMINRECOVERYOPERATION
DESCRIPTOR.message_types_by_name['StorageAdminResponse'] = _STORAGEADMINRESPONSE
DESCRIPTOR.message_types_by_name['AdminResponse'] = _ADMINRESPONSE
DESCRIPTOR.message_types_by_name['DictionaryKeys'] = _DICTIONARYKEYS
DESCRIPTOR.message_types_by_name['RequestContainer'] = _REQUESTCONTAINER
DESCRIPTOR.message_types_by_name['DictionaryLocation'] = _DICTIONARYLOCATION

class HashedStorageHeader(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _HASHEDSTORAGEHEADER
  
  # @@protoc_insertion_point(class_scope:HashedStorageHeader)

class StorageHeader(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STORAGEHEADER
  
  # @@protoc_insertion_point(class_scope:StorageHeader)

class StorageResponseHeader(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STORAGERESPONSEHEADER
  
  # @@protoc_insertion_point(class_scope:StorageResponseHeader)

class DictionaryResponseHeader(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DICTIONARYRESPONSEHEADER
  
  # @@protoc_insertion_point(class_scope:DictionaryResponseHeader)

class DataLocation(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DATALOCATION
  
  # @@protoc_insertion_point(class_scope:DataLocation)

class DictionaryHeader(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DICTIONARYHEADER
  
  # @@protoc_insertion_point(class_scope:DictionaryHeader)

class StorageAdminRequestContainer(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STORAGEADMINREQUESTCONTAINER
  
  # @@protoc_insertion_point(class_scope:StorageAdminRequestContainer)

class StorageAdminServerLocation(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STORAGEADMINSERVERLOCATION
  
  # @@protoc_insertion_point(class_scope:StorageAdminServerLocation)

class StorageAdminRecoveryOperation(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STORAGEADMINRECOVERYOPERATION
  
  # @@protoc_insertion_point(class_scope:StorageAdminRecoveryOperation)

class StorageAdminResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STORAGEADMINRESPONSE
  
  # @@protoc_insertion_point(class_scope:StorageAdminResponse)

class AdminResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ADMINRESPONSE
  
  # @@protoc_insertion_point(class_scope:AdminResponse)

class DictionaryKeys(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DICTIONARYKEYS
  
  # @@protoc_insertion_point(class_scope:DictionaryKeys)

class RequestContainer(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUESTCONTAINER
  
  # @@protoc_insertion_point(class_scope:RequestContainer)

class DictionaryLocation(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DICTIONARYLOCATION
  
  # @@protoc_insertion_point(class_scope:DictionaryLocation)

# @@protoc_insertion_point(module_scope)
