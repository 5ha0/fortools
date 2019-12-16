# This file is Copyright 2019 Volatility Foundation and licensed under the Volatility Software License 1.0
# which is available at https://www.volatilityfoundation.org/license/vsl-v1.0
#

import struct
from typing import Tuple, Optional

from volatility.framework import constants, exceptions, interfaces
from volatility.framework.layers import segmented
from volatility.framework.symbols import intermed


class WindowsCrashDump32FormatException(exceptions.LayerException):
    """Thrown when an error occurs with the underlying Crash file format."""


class WindowsCrashDump32Layer(segmented.SegmentedLayer):
    """A Windows crash format TranslationLayer.

    This TranslationLayer supports Microsoft complete memory dump files.
    It currently does not support kernel or small memory dump files.
    """

    provides = {"type": "physical"}

    SIGNATURE = 0x45474150
    VALIDDUMP = 0x504d5544
    _magic_struct = struct.Struct('<II')
    headerpages = 1

    def __init__(self, context: interfaces.context.ContextInterface, config_path: str, name: str) -> None:

        # Construct these so we can use self.config
        self._context = context
        self._config_path = config_path
        self._page_size = 0x1000
        self._base_layer = self.config["base_layer"]

        # Create a custom SymbolSpace
        self._crash_table_name = intermed.IntermediateSymbolTable.create(context, self._config_path, 'windows', 'crash')
        # Check Header
        hdr_layer = self._context.layers[self._base_layer]
        hdr_offset = 0
        self._check_header(hdr_layer, hdr_offset)

        # Need to create a header object
        self.header = self.context.object(self._crash_table_name + constants.BANG + "_DMP_HEADER",
                                          offset = hdr_offset,
                                          layer_name = self._base_layer)

        # Extract the DTB
        self.dtb = self.header.DirectoryTableBase

        # Verify that it is a supported format
        if self.header.DumpType != 0x1:
            raise WindowsCrashDump32FormatException(self.name,
                                                    "unsupported dump format 0x{:x}".format(self.header.DumpType))

        super().__init__(context, config_path, name)

    def _load_segments(self) -> None:
        """Loads up the segments from the meta_layer."""

        segments = []

        offset = self.headerpages
        for x in self.header.PhysicalMemoryBlockBuffer.Run:
            segments.append((x.BasePage * 0x1000, offset * 0x1000, x.PageCount * 0x1000))
            # print("Segments {:x} {:x} {:x}".format(x.BasePage * 0x1000,
            #                  offset * 0x1000,
            #                  x.PageCount * 0x1000))
            offset += x.PageCount

        if len(segments) == 0:
            raise WindowsCrashDump32FormatException(self.name,
                                                    "No Crash segments defined in {}".format(self._base_layer))

        self._segments = segments

    @classmethod
    def _check_header(cls, base_layer: interfaces.layers.DataLayerInterface, offset: int = 0) -> Tuple[int, int]:

        # Verify the Window's crash dump file magic
        try:
            header_data = base_layer.read(offset, cls._magic_struct.size)
        except exceptions.InvalidAddressException:
            raise WindowsCrashDump32FormatException(base_layer.name,
                                                    "Crashdump header not found at offset {}".format(offset))
        (signature, validdump) = cls._magic_struct.unpack(header_data)

        if signature != cls.SIGNATURE:
            raise WindowsCrashDump32FormatException(
                base_layer.name, "Bad signature 0x{:x} at file offset 0x{:x}".format(signature, offset))
        if validdump != cls.VALIDDUMP:
            raise WindowsCrashDump32FormatException(
                base_layer.name, "Invalid dump 0x{:x} at file offset 0x{:x}".format(validdump, offset))

        return (signature, validdump)


class WindowsCrashDump32Stacker(interfaces.automagic.StackerLayerInterface):
    stack_order = 11

    @classmethod
    def stack(cls,
              context: interfaces.context.ContextInterface,
              layer_name: str,
              progress_callback: constants.ProgressCallback = None) -> Optional[interfaces.layers.DataLayerInterface]:
        try:
            WindowsCrashDump32Layer._check_header(context.layers[layer_name])
        except WindowsCrashDump32FormatException:
            return None
        new_name = context.layers.free_layer_name("WindowsCrashDump32Layer")
        context.config[interfaces.configuration.path_join(new_name, "base_layer")] = layer_name
        return WindowsCrashDump32Layer(context, new_name, new_name)
