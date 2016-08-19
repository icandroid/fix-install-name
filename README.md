# fix-install-name
python script to fix install name of a binary | (dynamic library) for Mac OS

for knowledge of 'install name', please refer to
https://www.mikeash.com/pyblog/friday-qa-2009-11-06-linking-and-install-names.html
, it gives concise understanding of 'install name'.

when we install some libraries via 'automake', or 'cmake', sometimes the installed dynamic libraries are
not installed with effective install names.
in here, **ONLY ABSOLUTE PATH** is supported in changing/updating the install names.
if you feel necessary, you may extend the script to support '@rpath', '@loader_path', '@executable_path'.

please keep in mind that it is **your own risk** to run the script.

to run the script, just type like:
  `python fix-install-name.py [file_list]`

the 'file_list' is the list of files
