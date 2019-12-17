from fortools import Mem

file = Mem.mem_open("..\\CPO_PC.vmem")

'''
Uncomment the comment you want to use.
'''

# # Lists process command line arguments
# result = file.get_cmdline()
#
# # Dumps process memory ranges as DLLs
# result = file.get_dlldump()
#
# # Lists the loaded modules in a particular windows memory image
# result = file.get_dlllist()
#
# # List IRPs for drivers in a particular windows memory image
# result = file.get_driverirp()
#
# # Scans for drivers present in a particular windows memory image
# result = file.get_driverscan()
#
# # Scans for file objects present in a particular windows memory image
# result = file.get_filescan()
#
# # Lists process open handles
# result = file.get_handles()
#
# # Show OS & kernel details of the memory sample being analyzed
# result = file.get_info()
#
# # Scans for mutexes present in a particular windows memory image
# result = file.get_mutantscan()
#
# # Lists the processes present in a particular windows memory image
# result = file.get_pslist()
#
# # Plugin for listing processes in a tree based on their parent process ID
# result = file.get_pstree()
#
# # Scans for processes present in a particular windows memory image
# result = file.get_psscan()
#
# # Lists the certificates in the registry's Certificate Store
# result = file.get_reg_certificates()
#
# # Lists the registry hives present in a particular memory image
# result = file.get_reg_hivelist()
#
# # Scans for registry hives present in a particular windows memory image
# result = file.get_reg_hivescan()
#
# # Lists the registry keys under a hive or specific key value
# result = file.get_reg_printkey()
#
# # Print userassist registry keys and information
# result = file.get_reg_userassist()
#
# # Lists process memory ranges
# result = file.get_vadinfo()
#
#Lists process memory ranges that potentially contain injected code
result = file.get_malfind()

# #Dumps process executable images. (All)
# result = file.get_procdump('all', 'all')

# #Dumps process executable images. (PID)
# result = file.get_procdump('part', 'pid number')

## Runs all relevant plugins that provide time related information and orders the results by time
#result = file.timeliner()

for i in range(len(result)):
    print(result[i])





