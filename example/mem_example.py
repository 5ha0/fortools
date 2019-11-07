from fortools import Mem

file = Mem.mem_open("..\\dataset\\CPO_PC.vmem")
file.vol_path = "..\\forlib\\processing\\volatility\\vol.py"

# # Lists process command line arguments
# result = file.cmdline()
#
# # Dumps process memory ranges as DLLs
# result = file.dlldump()
#
# # Lists the loaded modules in a particular windows memory image
# result = file.dlllist()
#
# # List IRPs for drivers in a particular windows memory image
# result = file.driverirp()
#
# # Scans for drivers present in a particular windows memory image
# result = file.driverscan()
#
# # Scans for file objects present in a particular windows memory image
# result = file.filescan()
#
# Lists process open handles
result = file.handles()
#
# # Show OS & kernel details of the memory sample being analyzed
# result = file.info()
#
# # Scans for mutexes present in a particular windows memory image
# result = file.mutantscan()
#
# # Lists the processes present in a particular windows memory image
# result = file.pslist()
#
# # Plugin for listing processes in a tree based on their parent process ID
# result = file.pstree()
#
# # Scans for processes present in a particular windows memory image
# result = file.psscan()
#
# # Lists the certificates in the registry's Certificate Store
# result = file.reg_certificates()
#
# # Lists the registry hives present in a particular memory image
# result = file.reg_hivelist()
#
# # Scans for registry hives present in a particular windows memory image
# result = file.reg_hivescan()
#
# # Lists the registry keys under a hive or specific key value
# result = file.reg_printkey()
#
# # Print userassist registry keys and information
# result = file.reg_userassist()
#
# # Lists process memory ranges
# result = file.vadinfo()
#
# Lists process memory ranges that potentially contain injected code
# result = file.malfind()
## Runs all relevant plugins that provide time related information and orders the results by time
#result = file.timeliner()
for i in range(len(result)):
    print(result[i])





