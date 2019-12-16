# This file is Copyright 2019 Volatility Foundation and licensed under the Volatility Software License 1.0
# which is available at https://www.volatilityfoundation.org/license/vsl-v1.0
#

import logging
from typing import List, Iterator, Any

from volatility.framework import exceptions, interfaces
from volatility.framework import renderers, contexts
from volatility.framework.automagic import mac
from volatility.framework.configuration import requirements
from volatility.framework.interfaces import plugins
from volatility.framework.objects import utility
from volatility.framework.renderers import format_hints
from volatility.plugins.mac import lsmod

vollog = logging.getLogger(__name__)


class trustedbsd(plugins.PluginInterface):
    """Checks for malicious trustedbsd modules"""

    @classmethod
    def get_requirements(cls) -> List[interfaces.configuration.RequirementInterface]:
        return [
            requirements.TranslationLayerRequirement(name = 'primary',
                                                     description = 'Memory layer for the kernel',
                                                     architectures = ["Intel32", "Intel64"]),
            requirements.SymbolTableRequirement(name = "darwin", description = "Mac kernel symbols"),
            requirements.PluginRequirement(name = 'lsmod', plugin = lsmod.Lsmod, version = (1, 0, 0))
        ]

    def _generator(self, mods: Iterator[Any]):
        mac.MacUtilities.aslr_mask_symbol_table(self.context, self.config['darwin'], self.config['primary'])

        kernel = contexts.Module(self._context, self.config['darwin'], self.config['primary'], 0)

        policy_list = kernel.object_from_symbol(symbol_name = "mac_policy_list").cast("mac_policy_list")

        entries = kernel.object(object_type = "array",
                                offset = policy_list.entries.dereference().vol.offset,
                                subtype = kernel.get_type('mac_policy_list_element'),
                                count = policy_list.staticmax + 1)

        mask = self.context.layers[self.config['primary']].address_mask
        mods_list = [(mod.name, mod.address & mask, (mod.address & mask) + mod.size) for mod in mods]

        for i, ent in enumerate(entries):
            # I don't know how this can happen, but the kernel makes this check all over the place
            # the policy isn't useful without any ops so a rootkit can't abuse this
            try:
                mpc = ent.mpc.dereference()
                ops = mpc.mpc_ops.dereference()
            except exceptions.InvalidAddressException:
                continue

            try:
                ent_name = utility.pointer_to_string(mpc.mpc_name, 255)
            except exceptions.InvalidAddressException:
                ent_name = "N/A"

            for check in ops.vol.members:
                call_addr = getattr(ops, check)

                if call_addr is None or call_addr == 0:
                    continue

                found_module = None

                for mod_name_info, mod_base, mod_end in mods_list:
                    if call_addr >= mod_base and call_addr <= mod_end:
                        found_module = mod_name_info
                        break

                if found_module:
                    symbol_module = utility.array_to_string(found_module)
                else:
                    symbol_module = "UNKNOWN"

                yield (0, (check, ent_name, symbol_module, format_hints.Hex(call_addr)))

    def run(self):
        return renderers.TreeGrid([("Member", str), ("Policy Name", str), ("Handler Module", str),
                                   ("Handler Address", format_hints.Hex)],
                                  self._generator(
                                      lsmod.Lsmod.list_modules(self.context, self.config['primary'],
                                                               self.config['darwin'])))
