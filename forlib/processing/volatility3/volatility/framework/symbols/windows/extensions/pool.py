import functools
import struct
from typing import Optional, Tuple, List, Dict

from volatility.framework import objects, interfaces, constants, symbols, exceptions
from volatility.framework.renderers import conversion


class POOL_HEADER(objects.StructType):
    """A kernel pool allocation header.

    Exists at the base of the allocation and provides a tag that we can
    scan for.
    """

    def get_object(self,
                   type_name: str,
                   use_top_down: bool,
                   executive: bool = False,
                   native_layer_name: Optional[str] = None) -> Optional[interfaces.objects.ObjectInterface]:
        """Carve an object or data structure from a kernel pool allocation

        Args:
            type_name: the data structure type name
            native_layer_name: the name of the layer where the data originally lived
            object_type: the object type (executive kernel objects only)

        Returns:
            An object as found from a POOL_HEADER
        """

        symbol_table_name = self.vol.type_name.split(constants.BANG)[0]
        if constants.BANG in type_name:
            symbol_table_name, type_name = type_name.split(constants.BANG)[0:2]

        object_header_type = self._context.symbol_space.get_type(symbol_table_name + constants.BANG + "_OBJECT_HEADER")
        pool_header_size = self.vol.size

        # if there is no object type, then just instantiate a structure
        if not executive:
            mem_object = self._context.object(symbol_table_name + constants.BANG + type_name,
                                              layer_name = self.vol.layer_name,
                                              offset = self.vol.offset + pool_header_size,
                                              native_layer_name = native_layer_name)
            return mem_object

        # otherwise we have an executive object in the pool
        else:
            if symbols.symbol_table_is_64bit(self._context, symbol_table_name):
                alignment = 16
            else:
                alignment = 8

            # use the top down approach for windows 8 and later
            if use_top_down:
                body_offset = object_header_type.relative_child_offset('Body')
                infomask_offset = object_header_type.relative_child_offset('InfoMask')
                optional_headers, lengths_of_optional_headers = self._calculate_optional_header_lengths(
                    self._context, symbol_table_name)
                padding_available = None if 'PADDING_INFO' not in optional_headers else optional_headers.index(
                    'PADDING_INFO')
                max_optional_headers_length = sum(lengths_of_optional_headers)

                # define the starting and ending bounds for the scan
                start_offset = self.vol.offset + pool_header_size
                addr_limit = min(max_optional_headers_length, self.BlockSize * alignment)

                # A single read is better than lots of little one-byte reads.
                # We're ok padding this, because the byte we'd check would be 0 which would only be valid if there
                # were no optional headers in the first place (ie, if we read too much for headers that don't exist,
                # but the bit we could read were valid)
                infomask_data = self._context.layers[self.vol.layer_name].read(start_offset,
                                                                               addr_limit + infomask_offset,
                                                                               pad = True)

                # Addr stores the offset to the potential start of the OBJECT_HEADER from just after the POOL_HEADER
                # It will always be aligned to a particular alignment
                for addr in range(0, addr_limit, alignment):
                    infomask_value = infomask_data[addr + infomask_offset]

                    padding_present = False
                    optional_headers_length = 0
                    for i in range(len(lengths_of_optional_headers)):
                        if infomask_value & (1 << i):
                            optional_headers_length += lengths_of_optional_headers[i]
                            if i == padding_available:
                                padding_present = True

                    # PADDING_INFO is a special case (4 bytes that contain the total padding length)
                    padding_length = 0
                    if padding_present:
                        # Read the four bytes from just before the next optional_headers_length minus the padding_info size
                        #
                        #  ---------------
                        #  POOL_HEADER
                        #  ---------------
                        #
                        #  start of PADDING_INFO
                        #  ---------------
                        #  End of other optional headers
                        #  ---------------
                        #  OBJECT_HEADER
                        #  ---------------
                        if addr - optional_headers_length < 0:
                            continue
                        padding_length = struct.unpack(
                            "<I", infomask_data[addr - optional_headers_length:addr - optional_headers_length + 4])[0]
                        padding_length -= lengths_of_optional_headers[padding_available]

                    # Certain versions of windows have PADDING_INFO lengths that are too long
                    # So we now check that the padding length is at a minimum the right length
                    # and that it doesn't go beyond the entirety of the data
                    if addr - optional_headers_length >= padding_length > addr:
                        continue

                    try:
                        mem_object = self._context.object(symbol_table_name + constants.BANG + type_name,
                                                          layer_name = self.vol.layer_name,
                                                          offset = addr + body_offset + start_offset,
                                                          native_layer_name = native_layer_name)

                        if mem_object.is_valid():
                            return mem_object

                    except (TypeError, exceptions.InvalidAddressException):
                        pass

            # use the bottom up approach for windows 7 and earlier
            else:
                type_size = self._context.symbol_space.get_type(symbol_table_name + constants.BANG + type_name).size
                rounded_size = conversion.round(type_size, alignment, up = True)

                mem_object = self._context.object(symbol_table_name + constants.BANG + type_name,
                                                  layer_name = self.vol.layer_name,
                                                  offset = self.vol.offset + self.BlockSize * alignment - rounded_size,
                                                  native_layer_name = native_layer_name)

                try:
                    if mem_object.is_valid():
                        return mem_object
                except (TypeError, exceptions.InvalidAddressException):
                    return None
        return None

    @classmethod
    @functools.lru_cache()
    def _calculate_optional_header_lengths(cls, context: interfaces.context.ContextInterface,
                                           symbol_table_name: str) -> Tuple[List[str], List[int]]:
        headers = []
        sizes = []
        for header in [
                'CREATOR_INFO', 'NAME_INFO', 'HANDLE_INFO', 'QUOTA_INFO', 'PROCESS_INFO', 'AUDIT_INFO', 'EXTENDED_INFO',
                'HANDLE_REVOCATION_INFO', 'PADDING_INFO'
        ]:
            try:
                type_name = "{}{}_OBJECT_HEADER_{}".format(symbol_table_name, constants.BANG, header)
                header_type = context.symbol_space.get_type(type_name)
                headers.append(header)
                sizes.append(header_type.size)
            except:
                # Some of these may not exist, for example:
                #   if build < 9200: PADDING_INFO else: AUDIT_INFO
                #   if build == 10586: HANDLE_REVOCATION_INFO else EXTENDED_INFO
                # based on what's present and what's not, this list should be the right order and the right length
                pass
        return headers, sizes


class ExecutiveObject(interfaces.objects.ObjectInterface):
    """This is used as a "mixin" that provides all kernel executive objects
    with a means of finding their own object header."""

    def get_object_header(self) -> 'OBJECT_HEADER':
        if constants.BANG not in self.vol.type_name:
            raise ValueError("Invalid symbol table name syntax (no {} found)".format(constants.BANG))
        symbol_table_name = self.vol.type_name.split(constants.BANG)[0]
        body_offset = self._context.symbol_space.get_type(symbol_table_name + constants.BANG +
                                                          "_OBJECT_HEADER").relative_child_offset("Body")
        return self._context.object(symbol_table_name + constants.BANG + "_OBJECT_HEADER",
                                    layer_name = self.vol.layer_name,
                                    offset = self.vol.offset - body_offset,
                                    native_layer_name = self.vol.native_layer_name)


class OBJECT_HEADER(objects.StructType):
    """A class for the headers for executive kernel objects, which contains
    quota information, ownership details, naming data, and ACLs."""

    def is_valid(self) -> bool:
        """Determine if the object is valid."""

        # if self.InfoMask > 0x48:
        #    return False

        try:
            if self.PointerCount > 0x1000000 or self.PointerCount < 0:
                return False
        except exceptions.InvalidAddressException:
            return False

        return True

    def get_object_type(self, type_map: Dict[int, str], cookie: int = None) -> Optional[str]:
        """Across all Windows versions, the _OBJECT_HEADER embeds details on
        the type of object (i.e. process, file) but the way its embedded
        differs between versions.

        This API abstracts away those details.
        """

        if self.vol.get('object_header_object_type', None) is not None:
            return self.vol.object_header_object_type

        try:
            # vista and earlier have a Type member
            self._vol['object_header_object_type'] = self.Type.Name.String
        except AttributeError:
            # windows 7 and later have a TypeIndex, but windows 10
            # further encodes the index value with nt1!ObHeaderCookie
            try:
                type_index = ((self.vol.offset >> 8) ^ cookie ^ self.TypeIndex) & 0xFF
            except (AttributeError, TypeError):
                type_index = self.TypeIndex

            self._vol['object_header_object_type'] = type_map.get(type_index)
        return self.vol.object_header_object_type

    @property
    def NameInfo(self) -> interfaces.objects.ObjectInterface:
        if constants.BANG not in self.vol.type_name:
            raise ValueError("Invalid symbol table name syntax (no {} found)".format(constants.BANG))

        symbol_table_name = self.vol.type_name.split(constants.BANG)[0]

        try:
            header_offset = self.NameInfoOffset
        except AttributeError:
            # http://codemachine.com/article_objectheader.html (Windows 7 and later)
            name_info_bit = 0x2

            layer = self._context.layers[self.vol.native_layer_name]
            kvo = layer.config.get("kernel_virtual_offset", None)

            if kvo is None:
                raise AttributeError("Could not find kernel_virtual_offset for layer: {}".format(self.vol.layer_name))

            ntkrnlmp = self._context.module(symbol_table_name, layer_name = self.vol.layer_name, offset = kvo)
            address = ntkrnlmp.get_symbol("ObpInfoMaskToOffset").address
            calculated_index = self.InfoMask & (name_info_bit | (name_info_bit - 1))

            header_offset = self._context.object(symbol_table_name + constants.BANG + "unsigned char",
                                                 layer_name = self.vol.native_layer_name,
                                                 offset = kvo + address + calculated_index)

        header = self._context.object(symbol_table_name + constants.BANG + "_OBJECT_HEADER_NAME_INFO",
                                      layer_name = self.vol.layer_name,
                                      offset = self.vol.offset - header_offset,
                                      native_layer_name = self.vol.native_layer_name)
        return header
