# fortools
Continuous Update Scheduled

# Introduction
Fortools is a library for python Forensics. It is designed with Python for easy use by beginners to professionals, and improved usability by providing an integrated environment.

# Background
There are few free integrated Python libraries that can be used from a forensics perspective. So team 5ha0 offers an integrated Python library from a forensics perspective as an open source.

# Installation
'fortools' can be installed with pip install fortools.

# License 

# How to Use
For instructions, check the example folder.
And for beginners, we provide chatbot function. If you don't know how to use it, try typing it below.

```python
from fortools import *

Chatbot()
```

# Precautions
**Browser**  
You can get list of these files' analysis.
Chrome: Cache, History, Download, Cookies(version:)
Firefox: History, Download, Cookies (version:)
IE_Edge: Cache, History, Download, Cookies (version: more than 10)
Continue adding versions scheduled

**Registry**  
Currently, only the following analyses are provided: SAM, SOFTWARE, NTUSER.DAT, SYSTEM File(System File is on progress)

**Disk**  
If you extract file in disk, you need to check start sector with volume_metadata() function's data.

**Memory**  
You need to install volatility3. Plz download it and put it in path forlib/processing. This analysis is only available for the current window memory file.

# Contact
If you have any questions , feel free to send us an e-mail(fortools.official@gmail.com).
