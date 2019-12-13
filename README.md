# fortools
Continuous Update Scheduled

# Introduction
Fortools is a library for python Forensics. It is designed with Python for easy use by beginners to professionals, and improved usability by providing an integrated environment.

# Background
There are few free integrated Python libraries that can be used from a forensics perspective. So team 5ha0 offers an integrated Python library from a forensics perspective as an open source.

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

**Recycle**  
This module will analyze only $I files among the recycle bin files. And now, this module analyzes Windows 7/8/10.
  About functions  
->show_all_info/get_all_info: json format(file name, header contents(read as little endian binary), file size, original path and deleted time)<br>

**Iconcache**  
Now, this module analyzes Windows 7/10. And parse only meanigful contents in forensics.
This module will analyze only iconcache.db files. If you want to analyze other files like iconcache_##.db, you can use *thumbnail analysis*.
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

**Files**
- get_info(JPEG): [time, Latitude, Longitude]
- get_info(PDF): [author, creator, creation, modification, TimeZone]
- get_info(HWP): [Author, Date, Last Save, Create Time, Last Save Time]
- get_info(MS Old version): [title, Author, Create Time, Last Save, Last Save Time, creating_application]

 
# Contact
If you have any questions , feel free to send us an e-mail(fortools.official@gmail.com).
