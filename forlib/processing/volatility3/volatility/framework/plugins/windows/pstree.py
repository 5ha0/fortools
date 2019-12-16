# This file is Copyright 2019 Volatility Foundation and licensed under the Volatility Software License 1.0
# which is available at https://www.volatilityfoundation.org/license/vsl-v1.0
#

from typing import Dict, Set

from volatility.framework import objects, interfaces
from volatility.framework.renderers import format_hints
from volatility.plugins.windows import pslist


class PsTree(pslist.PsList):
    """Plugin for listing processes in a tree based on their parent process
    ID."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._processes = {}  # type: Dict[int, interfaces.objects.ObjectInterface]
        self._levels = {}  # type: Dict[int, int]
        self._children = {}  # type: Dict[int, Set[int]]

    def find_level(self, pid: objects.Pointer) -> None:
        """Finds how deep the pid is in the processes list."""
        seen = set([])
        seen.add(pid)
        level = 0
        proc = self._processes.get(pid, None)
        while proc is not None and proc.InheritedFromUniqueProcessId not in seen:
            child_list = self._children.get(proc.InheritedFromUniqueProcessId, set([]))
            child_list.add(proc.UniqueProcessId)
            self._children[proc.InheritedFromUniqueProcessId] = child_list
            proc = self._processes.get(proc.InheritedFromUniqueProcessId, None)
            level += 1
        self._levels[pid] = level

    def _generator(self):
        """Generates the Tree of processes."""
        for proc in self.list_processes(self.context, self.config['primary'], self.config['nt_symbols']):

            if not self.config.get('physical', self.PHYSICAL_DEFAULT):
                offset = proc.vol.offset
            else:
                layer_name = self.config['primary']
                memory = self.context.layers[layer_name]
                (_, offset, _, _) = list(memory.mapping(offset = proc.vol.offset, length = 0))[0]

            self._processes[proc.UniqueProcessId] = proc

        # Build the child/level maps
        for pid in self._processes:
            self.find_level(pid)

        def yield_processes(pid):
            proc = self._processes[pid]
            row = (proc.UniqueProcessId, proc.InheritedFromUniqueProcessId,
                   proc.ImageFileName.cast("string", max_length = proc.ImageFileName.vol.count, errors = 'replace'),
                   format_hints.Hex(offset), proc.ActiveThreads, proc.get_handle_count(), proc.get_session_id(),
                   proc.get_is_wow64(), proc.get_create_time(), proc.get_exit_time())

            yield (self._levels[pid] - 1, row)
            for child_pid in self._children.get(pid, []):
                yield from yield_processes(child_pid)

        for pid in self._levels:
            if self._levels[pid] == 1:
                yield from yield_processes(pid)
