# Description

Script that will parse a PDF from banks, then renaming it appropriately

Only supports one bank:
* Norway - Sparebank 1 - SR Bank

# Building Executable

```
pip install -U pyinstaller
pyinstaller --onefile rename_pdf.py
```

Copy this file to somewhere on your path, e.g. c:\windows\system32

# Usage with Total Commander

This script was build to be used with Total Commander.

1. Right-click the menu bar and choose "Change"
1. Click "Add" to add a button to the bar
1. Fill in as follows:
  * Command: ```c:\windows\system32\rename_pdf.exe```
  * Parameters: ```--from %P --to %T --mode move```
  * Icon File: ```C:\Windows\System32\rename_pdf.exe```
  * Check 'Run Minimized'

