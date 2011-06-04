import argparse
import imp
import marshal
import os
import struct
import sys
import time

import pefile

IGNORE = [
        '<install zipextimporter>.pyc', # zip importer added by py2exe
    ]

def __timestamp():
    """Generate timestamp data for pyc header."""
    today = time.time()
    ret = struct.pack('L', int(today))
    return ret

def __build_magic(magic):
    """Build Python magic number for pyc header."""
    return struct.pack('Hcc', magic, '\r', '\n')

def __current_magic():
    """Current Python magic number."""
    return imp.get_magic()

versions = {
    # version, magic (see Python/import.c)
    '1.5': __build_magic(20121),
    '1.6': __build_magic(50428),
    '2.0': __build_magic(50823),
    '2.1': __build_magic(60202),
    '2.2': __build_magic(60717),
    '2.3': __build_magic(62011),
    '2.4': __build_magic(62061),
    '2.5': __build_magic(62131),
    '2.6': __build_magic(62161),
    '2.7': __build_magic(62191),
}


def get_scripts_resource(pe):
    """Return the PYTHONSCRIPT resource entry."""
    res = None
    for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if entry.name and entry.name.string == u"PYTHONSCRIPT":
            res = entry.directory.entries[0].directory.entries[0]
            break
    return res

def resource_dump(pe, res):
    """Return the dump of the given resource."""
    rva = res.data.struct.OffsetToData
    size = res.data.struct.Size

    dump = pe.get_data(rva, size)
    return dump

def get_co_from_dump(data):
    """Return the code objects from the dump."""
    # Read py2exe header
    current = struct.calcsize('iiii')
    metadata = struct.unpack('iiii', data[:current])

    # check py2exe magic number
    # assert(metadata[0] == 0x78563412)
    print "Magic value: %x" % metadata[0]
    print "Code bytes length: %d" % metadata[3]

    arcname = ""
    while data[current] != "\000":
        arcname += data[current]
        current += 1
    print "Archive name: %s" % (arcname or '-')

    code_bytes = data[current + 1:-2]
    # verify code bytes count and metadata info
    # assert(len(code_bytes) == metadata[3])

    code_objects = marshal.loads(code_bytes)
    return code_objects

def save_co_to_pyc(co, version, output_dir):
    """Save the code object as pyc file."""
    pyc_header = version + __timestamp()
    pyc_basename = os.path.basename(co.co_filename)
    pyc_name = pyc_basename + '.pyc'

    if pyc_name not in IGNORE:
        print "Extracting %s" % pyc_name
        destination = os.path.join(output_dir, pyc_name)
        pyc = open(destination, 'wb')
        pyc.write(pyc_header)
        marshaled_code = marshal.dumps(co)
        pyc.write(marshaled_code)
        pyc.close()

def unpy2exe(filename, python_version=None, output_dir=None):
    """Process input params and produce output pyc files."""
    if python_version is None:
        version = __current_magic()
    else:
        version = versions.get(python_version, __current_magic())

    if output_dir is None:
        output_dir = '.'
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pe = pefile.PE(filename)
    script_res = get_scripts_resource(pe)
    dump = resource_dump(pe, script_res)
    code_objects = get_co_from_dump(dump)
    for co in code_objects:
        save_co_to_pyc(co, version, output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract pyc files from py2exe executable.')
    parser.add_argument('filename', help='The py2exe executable')
    parser.add_argument('-o', '--output-dir', default='.',
        help="Output directory")
    parser.add_argument('-p', '--python-version', default=None,
        help="Python version for pyc")
    args = vars(parser.parse_args())
    unpy2exe(**args)

