# Description

Script that will parse a PDF from banks, then renaming it appropriately

Only supports one bank:
* Norway - Sparebank 1 - SR Bank

# Optional Configuration

You can add optional config by creating a config.py file, and adding blocks to this file

## Account aliases

You can add named aliases to account numbers as follows

```python
config.py
...
account_alias= {
    "1234.56.78901":"Savings",
    "1111.22.33333":"Billing"
}
...
```

# Building Executable

First you must have pyinstaller installed
```
pip install -U pyinstaller
```

Then cleanup and build the executable
```
rmdir dist /s /q
rmdir build /s /q
pyinstaller --onefile rename_pdf.py
```

Copy the created file from the dist folder to somewhere on your path, e.g. c:\windows\system32
```
copy dist\rename_pdf.exe c:\Windows\System32
```

# Usage with Total Commander

This script was build to be used with Total Commander.

1. Right-click the menu bar and choose "Change"
1. Click "Add" to add a button to the bar
1. Fill in as follows:
  * Command: ```c:\windows\system32\rename_pdf.exe```
  * Parameters: ```--from %P --to %T --mode move```
  * Icon File: ```C:\Windows\System32\rename_pdf.exe```
  * Check 'Run Minimized'

