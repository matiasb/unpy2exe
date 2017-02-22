unpy2exe
========

```
usage: unpy2exe.py [-h] [-o OUTPUT_DIR] [-p PYTHON_VERSION] filename

Extract pyc files from py2exe executable.

positional arguments:
  filename              The py2exe executable

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory
  -p PYTHON_VERSION, --python-version PYTHON_VERSION
                        Python version for pyc
  -v, --verbose         Verbose output
```

You can install it from PyPI:

```
$ pip install unpy2exe
```

Install from source
-------------------

Dependencies:
 - pefile
 - six
 - argparse (Python < 2.7)

You can install dependencies through `pip install -r requirements.txt`


Notes
-----

For .exe files generated with Python 2.x, you will need to run unpy2exe with
Python 2.x; similarly, for Python 3.x .exe files, you will need to run unpy2exe
with Python 3.x. Note the same unpy2exe source code works for both, but you
will need to install the dependencies accordingly.

On the other hand, to be able to run the extracted .pyc file, you will need the
same Python version used to generate the .exe, or at least the same major
version (although it is highly probable you could still get some issues or
crashes if the version doesn't match the original bytecode).


TODO:
 - Extract archived files (from zip/from exe)

See also:
 - http://py2exe.svn.sourceforge.net/viewvc/py2exe/trunk/py2exe/py2exe/build_exe.py?view=markup
