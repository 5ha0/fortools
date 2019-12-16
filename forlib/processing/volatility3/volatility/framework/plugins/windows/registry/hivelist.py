# This file is Copyright 2019 Volatility Foundation and licensed under the Volatility Software License 1.0
# which is available at https://www.volatilityfoundation.org/license/vsl-v1.0
#
import logging
from typing import Iterator, List, Tuple, Iterable, Optional

from volatility.framework import renderers, interfaces, exceptions
from volatility.framework.configuration import requirements
from volatility.framework.layers import registry
from volatility.framework.renderers import format_hints

vollog = logging.getLogger(__name__)


class HiveList(interfaces.plugins.PluginInterface):
    """Lists the registry hives present in a particular memory image."""

    _version = (1, 0, 0)

    @classmethod
    def get_requirements(cls) -> List[interfaces.configuration.RequirementInterface]:
        return [
            requirements.TranslationLayerRequirement(name = 'primary',
                                                     description = 'Memory layer for the kernel',
                                                     architectures = ["Intel32", "Intel64"]),
            requirements.SymbolTableRequirement(name = "nt_symbols", description = "Windows kernel symbols"),
            requirements.StringRequirement(name = 'filter',
                                           description = "String to filter hive names returned",
                                           optional = True,
                                           default = None)
        ]

    def _generator(self) -> Iterator[Tuple[int, Tuple[int, str]]]:
        for hive in self.list_hive_objects(context = self.context,
                                           layer_name = self.config["primary"],
                                           symbol_table = self.config["nt_symbols"],
                                           filter_string = self.config.get('filter', None)):

            yield (0, (format_hints.Hex(hive.vol.offset), hive.get_name() or ""))

    @classmethod
    def list_hives(cls,
                   context: interfaces.context.ContextInterface,
                   base_config_path: str,
                   layer_name: str,
                   symbol_table: str,
                   filter_string: Optional[str] = None,
                   hive_offsets: List[int] = None) -> Iterable[registry.RegistryHive]:
        """Walks through a registry, hive by hive returning the constructed
        registry layer name.

        Args:
            context: The context to retrieve required elements (layers, symbol tables) from
            layer_name: The name of the layer on which to operate
            symbol_table: The name of the table containing the kernel symbols
            filter_string: An optional string which must be present in the hive name if specified 
            offset: An optional offset to specify a specific hive to iterate over (takes precedence over filter_string)

        Yields:
            A registry hive layer name
        """
        if hive_offsets is None:
            try:
                hive_offsets = [
                    hive.vol.offset for hive in cls.list_hive_objects(context, layer_name, symbol_table, filter_string)
                ]
            except ImportError:
                vollog.warning("Unable to import windows.hivelist plugin, please provide a hive offset")
                raise ValueError("Unable to import windows.hivelist plugin, please provide a hive offset")

        for hive_offset in hive_offsets:
            # Construct the hive
            reg_config_path = cls.make_subconfig(context = context,
                                                 base_config_path = base_config_path,
                                                 hive_offset = hive_offset,
                                                 base_layer = layer_name,
                                                 nt_symbols = symbol_table)

            try:
                hive = registry.RegistryHive(context, reg_config_path, name = 'hive' + hex(hive_offset))
            except exceptions.InvalidAddressException:
                vollog.warning("Couldn't create RegistryHive layer at offset {}, skipping".format(hex(hive_offset)))
                continue
            context.layers.add_layer(hive)
            yield hive

    @classmethod
    def list_hive_objects(cls,
                          context: interfaces.context.ContextInterface,
                          layer_name: str,
                          symbol_table: str,
                          filter_string: str = None) -> Iterator[interfaces.objects.ObjectInterface]:
        """Lists all the hives in the primary layer.

        Args:
            context: The context to retrieve required elements (layers, symbol tables) from
            layer_name: The name of the layer on which to operate
            symbol_table: The name of the table containing the kernel symbols
            filter_string: A string which must be present in the hive name if specified

        Returns:
            The list of registry hives from the `layer_name` layer as filtered against using the `filter_string`
        """

        # We only use the object factory to demonstrate how to use one
        kvo = context.layers[layer_name].config['kernel_virtual_offset']
        ntkrnlmp = context.module(symbol_table, layer_name = layer_name, offset = kvo)

        list_head = ntkrnlmp.get_symbol("CmpHiveListHead").address
        list_entry = ntkrnlmp.object(object_type = "_LIST_ENTRY", offset = list_head)
        reloff = ntkrnlmp.get_type("_CMHIVE").relative_child_offset("HiveList")
        cmhive = ntkrnlmp.object(object_type = "_CMHIVE", offset = list_entry.vol.offset - reloff, absolute = True)

        # Run through the list forwards
        seen = set()
        traverse_backwards = False
        try:
            for hive in cmhive.HiveList:
                if filter_string is None or filter_string.lower() in str(hive.get_name() or "").lower():
                    if context.layers[layer_name].is_valid(hive.vol.offset):
                        seen.add(hive.vol.offset)
                        yield hive
        except exceptions.InvalidAddressException:
            vollog.warning("Hivelist failed traversing the list forwards, traversing backwards")
            traverse_backwards = True

        if traverse_backwards:
            try:
                for hive in cmhive.HiveList.to_list(cmhive.vol.type_name, "HiveList", forward = False):
                    if filter_string is None or filter_string.lower() in str(
                            hive.get_name() or "").lower() and hive.vol.offset not in seen:
                        if context.layers[layer_name].is_valid(hive.vol.offset):
                            yield hive
            except exceptions.InvalidAddressException:
                vollog.warning("Hivelist failed traversing the list backwards, giving up")

    def run(self) -> renderers.TreeGrid:
        return renderers.TreeGrid([("Offset", format_hints.Hex), ("FileFullPath", str)], self._generator())
