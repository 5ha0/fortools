# fortools
Continuous Update Scheduled

# Introduction
Fortools is a library for python Forensics. 
There are few free integrated Python libraries that can be used from a forensics perspective. So team 5ha0 offers an integrated Python library from a forensics perspective as an open source. It is designed with Python for easy use by beginners to professionals, and improved usability by providing an integrated environment.  

# Installation
'fortools' can be installed with *pip install fortools*.

# License 
GNU General Public License version 3.0 (GPLv3)

# How to Use
For instructions, check the example folder.
And for beginners, we provide chatbot function. If you don't know how to use it, try typing it below.

```python
from fortools import *

Chatbot()
```

When you open an editor, you must enable it with administrator privileges.

# Basic Path
**Event Log**  
C:\Windows\System32\winevt\Logs\Security.evtx

**Jump List**  
%UserProfile%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations

**Filesystem Log**  
$UsnJrnl : C:\$Extend\$Usnjrnl:$J  
$MFT : C:\$MFT  
$LogFile : C:\$LogFile  

**Registry**  
SAM, SOFTWARE, SECURITY, SYSTEM: C:\Windows\System32\Config  
NTUSER.DAT: %UserProfile% 

**Browser**  
*Chrome*  
Cache: %UserProfile%\AppData\Local\Google\Chrome\User Data\Default(or some Profile)\Cache(folder)  
History, Download: %UserProfile%\AppData\Local\Google\Chrome\User Data\Default(or some Profile)\History  
Cookies: %UserProfile%\AppData\Local\Google\Chrome\User Data\Default(or some Profile)\Cookies  

*Firefox*  
Cookies: %UserProfile%\AppData\Roaming\Mozilla\Firefox\Profiles -> random number\cookies.sqlite  
History, Download: %UserProfile%\AppData\Roaming\Mozilla\Firefox\Profiles -> random number\places.sqlite  

*IE && Edge*  
 %UserProfile%AppData\Local\Microsoft\Windows\WebCache\WebCacheV01.dat
 
**Thumbcache__x.db && iconcache_xx.db**   
C:\Users\"username"\AppData\Local\Microsoft\Windows\Explorer(windows 10)  
 
**Prefetch**   
%SystemRoot%\Prefetch  

**Iconcache**   
%UserProfile%\AppData\Local\IconCache.db  

**Lnk**  
C:\USERS<user name>\AppData\Roaming\Microsoft\Windows\Recent  
 
**Recycle**   
C:\$Recycle.Bin\[USER SID]  
-> [USER SID] can be identified by typing whoami /user in the cmd window.  
-> domain accounts: wmic UserAccount Where LocalAccount=True Get SID

# Precautions
**Browser**  
You can get list of these files' analysis.
Chrome: Cache, History, Download, Cookies(version:)
Firefox: History, Download, Cookies (version:)
IE_Edge: Cache, History, Download, Cookies (version: more than 10)
Continue adding versions scheduled

**Registry**  
Currently, only the following analyses are provided: SAM, SOFTWARE, NTUSER.DAT, SYSTEM File(System File is on progress)  
If the key position you want to find is extended, it may be slow.  
ex) find_key("Uninstall") --> Microsoft\\Windows\\CurrentVersion\\Uninstall (this key location is 4th)  

**Disk**  
If you extract file in disk, you need to check start sector with volume_metadata() function's data.

**Memory**   
You need to install volatility3. Plz download it and put it in path forlib/processing. This analysis is only available for the current window memory file. 

When using a procdump, it must be entered in the following format
- all procdump : get_procdump('all', 'all')
- part procdump : get_procdump('part', 'pid number')
(please, this pid number's type is str)

When using a vaddump, it must be entered in the following format
- all vaddump : get_vaddump('all', 'all', 'all')
- part vaddump (you know pid number) : get_vaddump('part', 'all', 'pid number')
- part vaddump (you know pid number and address) : get_vaddump('part', 'address number', 'pid number')
(please, this pid number's type and address number's type are str)

**Recycle**  
This module will analyze only $I files among the recycle bin files. And now, this module analyzes Windows 7/8/10.
  About functions  
->show_all_info/get_all_info: json format(file name, header contents(read as little endian binary), file size, original path and deleted time)<br>

**Iconcache**  
Now, this module analyzes Windows 7/10. And parse only meanigful contents in forensics.
This module will analyze only iconcache.db files. If you want to analyze other files like iconcache_##.db, you can use *thumbnail analysis*.  
*File section information*  
- First Section: The path information for icons that are installed by default during Windows installation, and the application that users view or run, are stored in order.
- Second Section: Path information for links or short icons is saved.
- Third Section: After Windows is installed, icon path information for applications that you have run, viewed, and copied is saved in order.
  About functions  
->extension_filter: you can find file path of specific extension file<br>

**Prefetch**  
Now, this module analyzes Windows 7/10. And parse only meanigful contents in forensics.
  About functions  
->extension_filter_pf: you can find file path of specific extension file<br>
 
 **Lnk**  
Now, this module analyzes Windows 7/10. And parse only meanigful contents in forensics.

# Key Info
**Event Log**  
- [Idx, eventID, create Time, TimeZone, level, source, computer Info, SID]

**JumpList**  
- get_info: [TimeZone, create time, access time, write time, file size, target file size, Local Path, drive type, drive serial number, Volume Label]  
- get_summary: [Total Num of JumpList, otal Num of Add/Delete/Open action, Netbios, TimeZone, Last Access Time, Access Count, Data String]  
- get_destlist_data:[MAC(new), MAC(birth), netbios, TimeZone, last access time, access count, data]  

**Filesystem Log**  
- get_info($MFT): [LSN, TimeZone, SIN Creation Time, SIN Modified Time, SIN MFT Modified Time, SIN Last Accessed Time, FIN Creation Time, FIN Modified Time, FIN MFT Modified Time, FIN Last Accessed Time, File Size, Name, Parent]  
- get_info($J): [USN, TimeZone, Time, Source, File Attribute, Filename]  

**Thumbcache && Iconcache**
- get_info: [num, file_name, entry_hash, size, dimension, header_checksum, data_checksum, system, location]  
- dimension: [width, height]

**Files**  
- get_info(JPEG): [time, Latitude, Longitude]
- get_info(PDF): [author, creator, creation, modification, TimeZone]
- get_info(HWP): [Author, Date, Last Save, Create Time, Last Save Time]
- get_info(MS Old version): [title, Author, Create Time, Last Save, Last Save Time, creating_application]  
- get_info(ZIP): [TimeZone, Modified, System, version, Compressed, Uncompressed, CRC, Volume, Internal attr, External attr, Header offset, Flag bits, Raw time]  

**Disk**  
- get_info: [file_name, file_type, Type, size, ctime, mtime, atime, chage time]  
- e01_metadata:  [case_number, description, examiner_name, evidence_number, notes, acquiry_date, system_date, acquiry_operating_system, acquiry_software_Version, extents, Bytes per Sector, Number of Sector, Total Size, MD5, SHA1]  
- volume_metadata : [Type, Num, Start Sector, Total Sector, Size]  

**Registry**  
- find_key : [Last Written Time, Search Keyword, Root Key, Search Key Path]  
*Favorite.NTAnalysis*  
- get_recent_docs : [time, TimeZone, name, data]  
- get_recent_MRU : [time, TimeZone, name, data]  
- get_IE_visit  : [time, TimeZone, data]  
- get_ms_office : [Version, MS Key Last Written time, TimeZone, path]  
- get_userassist : [Time, TimeZone, Run Count, file]  
- get_HWP : [Viersion, TimeZone, MS Key Last Wrtten time, Name, Path]
*Favorite.SYSAnalysis*
- get_computer_info : [ICSDomain, DataBasePath, Hostname, DhcpNameServer, DhcpDomain]  
- get_USB : [Device Name, DeviceDesc, Capabilities, HardwareID, CompatibleIDs, ContainerID, ConfigFlags, ClassGUID, Driver, Class, Mfg, Service, FriendlyName]  
- get_timezone : [Bias, TimeZoneKeyName, ActiveTimeBias]  
- get_network_info : [Domain, IPAddress, DhcpIPAddress, DhcpServer, DhcpSubnetMask]  

*Favorite.SWAnalysis*
- get_os_info : [CurrentVersion, CurrentBuild, InstallDate, TimeZone, RegisteredOwner, EditionID, ProductName]  
- get_network_info : [ServiceName, Description]  

*Favorite.SAMAnalysis*
- last_login : [Last Login, Last PW Change, Log Fail Time, TimeZone, RID, Logon Success Count, Logon Fail Count, UserName]  
- user_name : [UserName, Last Written Time, TimeZone]  
- user_info : [Last Login, Last PW Change, Log Fail Time, TimeZone, RID, Logon Success Count, Logon Fail Count, UserName]  

**Memory**
- cmdline : [PID, Process, Args]  
- dlldump : [PID, Process, Result]  
- procdump : [PID, Process, Result]
- dlllist : [PID, Process, Base, Size, Name, Path]  
- driverirp : [Offset, Driver Name, IRP, Address, Module, Symbol]  
- driverscan : [Offset, Start, Size, Service Key, Driver Name, Name]  
- filescan : [Offset, Name]  
- handles : [PID, Process, Offset, HandleValue, Type, GrantendAccess, Name]  
- info : [Variable, Value]  
- mutantscan : [Offset, Name]  
- malfind : [PID, Process, Start, End, Tag, Protection, CommitCharge, PrivateMemory, HexDump, Disasm]  
- pslist : [PID, PPID, ImageFileName, Offset(V), Threads, Handles, SessionId, Wow64, CreateTime, ExitTime]  
- psscan : [PID, PPID, ImageFileName, Offset(V), Threads, Handles, SessionId, Wow64, CreateTime, ExitTime]  
- pstree : [PID, PPID, ImageFileName, Offset(V), Threads, Handles, SessionId, Wow64, CreateTime, ExitTime]  
- reg_certificates : [Certificate Path, Certificate Section, Certificate ID, Certificate Name]  
- reg_hivelist : [Offset, FileFullPath]  
- reg_hivescan : [Offset]  
- reg_printkey : [Last Write Time, Hive Offset, Type, Key, Name, Data, Volatile]  
- reg_userassist : [only print]  
- vadinfo : [PID, Process, Offset, Start VPN, End VPN, Tag, Protection, CommitCharge, PrivateMemory, Parent, File]  
- timeliner : [Plugin, Description, Created Date, Modified Date, Accessed Date, Changed Date]  

**Browser**  
- Cache: [index, type, browser, timezone, file_name, url, access_time, creation_time, file_size, file_path, expiry_time, last_modified_time, server_info]  
- Download: [index, type, browser, timezone, file name, download_path, download_start_time, download_end_time, file_size, url, guid, opened, state]  
- History: [index, type, browser, timezone, title, url, from_visit, keyword_search, visit_time, visit_count, visit_type]  
- Cookie: [index, type, browser, timezone, name, value, creation_time, last_accessed_time, expiry_time, host, path, is_secure, is_httponly]  

**Recycle**  
- ['$I Name','File Header','Original File Size','File Deleted Time','Time Zone','Original File Path']  

**Prefetch**  
- ['Executable File Name', 'Ref_file#', 'Num Metadata Records', 'Volume Device Path', 'Volume Creation Time', 'Volume Creation TimeZone', 'Volume Serial Num', 'File Last Launch Time#', 'File Last Launch TimeZone#', 'File Create Time', 'File Create TimeZone', 'File Write Time', 'File Write TimeZone', 'File Run Count']  

**Iconcache**  
- ['File Version', 'Section One Path Num', 'Section One Path#', 'Section One Icon image location#', 'Section Two Path Num', 'Section Two Path#', 'Section Two Icon image location#', 'Section Three Path Num', 'Section Three Path#', 'Section Three Icon image location#']  

**Lnk**  
- ['File Attributes0', 'Target File Creation Time', 'Target File Creation TimeZone', 'Target File Access Time', 'Target File Access TimeZone', 'Target File Write Time', 'Target File Write TimeZone', 'Link File Creation Time', 'Link File Creation TimeZone', 'Link File Last Access Time', 'Link File Last Access TimeZone', 'Link File Write Time', 'Link File Write TimeZone', 'Target File Size', 'IconIndex', 'Show Command', 'Drivetype', 'Driveserialnumber', 'Volumelable', 'Localbasepath Unicode', 'Localbasepath', 'NetName', 'DeviceName', 'NetworkProviderType', 'NetBios', 'Droid', 'DroidBirth']  


# Contact
If you have any questions , feel free to send us an e-mail(fortools.official@gmail.com).
