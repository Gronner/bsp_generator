#!/usr/local/bin/python3
"""
Author: Felix Bräunling <Gronner@t-online.de>
Creation Date: 2018-05-04
Description: A BSP-file generator. Takes a comma seperated value file and
             generates a header file using #define.
Style-Guide: PEP8
"""
import csv
import sys
import getopt


HEAD_INCLUDE_GUARD = '#ifndef __BSP_INCLUDED__\n#define __BSP_INCLUDED__\n'
BOT_INCLUDE_GUARD = '\n#endif //__BSP_INCLUDED__'
HEAD_DOCSTRING = ("/* -------------------------------------------- *\n"
                  " * This an is automatic generated file.         *\n"
                  " * Do not alter it, change the specification csv*\n"
                  " * instead.                                     *\n"
                  " * -------------------------------------------- */\n"
                  "\n")

ARGSTRING = 'i:o:'
ARGLIST = ['input=', 'output=', 'docstring=', 'include=']


def specification_file_read(spec_file_name):
    """
    Returns the input from a CSV file as a dictionary.
    Args:
        - spec_file_name (String): Path to the CSV file.
    Returns:
        - (Dictionary(String:String)): Returns a list of Dictionaries mapping
          the tables row entrys to the column headers.
    """
    entries = []

    with open(spec_file_name, 'r') as spec_file:
        csvreader = csv.DictReader(spec_file, delimiter=',', quotechar='"')
        for row in csvreader:
            entries.append(row)

    return entries


def _build_line(entry):
    """
    Create a define statement in a single line.
    Args:
        - entry(Dictionary(String:String)): Dictionary containing a description
          of the target define statement using the Keys: 'Module', 'Address/Value',
          'Function', 'Submodule' (opt), 'Comment' (opt)
    Returns:
        - (String): Define statement of the form:
          #define Module_Submodule_Function Address/Value // Comment
    """
    line = '#define '
    line += '{}_'.format(entry['Module'])
    if entry['Submodule']:
        line += '{}_'.format(entry['Submodule'])
    line += entry['Function']
    line += ' {} '.format(entry['Address/Value'])
    if entry['Comment']:
        line += '// {}'.format(entry['Comment'])
    line += '\n'
    return line


def _build_module_seperator(module, submodule=''):
    """
    Creates a string line with a seperator for module and submodule.
    Args:
        - module (String): Name of the module for the seperator
        - submodule (String): Name of the submodule for the seperator (default: empty string)
    Returns:
        - (String): Seperator of the form: // Defines for module->submodule
    """
    line = '\n// Defines for {}'.format(module)
    if submodule:
        line += '-> {}'.format(submodule)
    line += '\n'
    return line


def _build_import_header(imports):
    """
    Creates an import header for a list of libraries.
    Args:
        - imports (List(String)): List of n libraries, e.g. 'stdlib', 'time'
    Returns:
        - (String): n lines of the form: #include <library.h>
    """
    header = ''
    for lib in imports:
        header += '#include <{}.h>\n'.format(lib)
    header += '\n'
    return header


def bsp_file_write(bsp_file_name, imports, entries):
    """
    Writes the configuration to a header file based on the libraries to import and
    the specified define statements.
    Args:
        - bsp_file_name (String): Target header file
        - imports (List(String)): List of libraries to import, e.g. 'stdlib', 'time'
        - entries (List(Dictionary(String:String))): Dictionaries containing the
          description of the desired define statements with the keys:
          'Module', 'Address/Value', 'Function', 'Submodule' (opt), 'Comment' (opt)
    """
    with open(bsp_file_name, 'w') as bsp_file:
        current_module = ''
        current_submodule = ''

        bsp_file.write(HEAD_INCLUDE_GUARD)
        bsp_file.write(HEAD_DOCSTRING)
        if imports:
            bsp_file.write(_build_import_header(imports))

        for entry in entries:
            if current_module != entry['Module'] or \
               current_submodule != entry['Submodule']:
                current_module = entry['Module']
                current_submodule = entry['Submodule']
                bsp_file.write(_build_module_seperator(entry['Module'],
                                                       entry['Submodule']))
            bsp_file.write(_build_line(entry))

        bsp_file.write(BOT_INCLUDE_GUARD)

def create_docstring(docstring_file_name):
    """
    Instead of using the default header comment a file containing a custom
    on can be used to generate the header comment.
    Args:
        - docstring_file_name (String): Path to the text file containing the
          header comment without comment markers (// or /* */)
    Returns:
        - (String): The header comment specified in the input file enclosed by
          a multi line comment enclosue (/* */)
    """
    lines = ''
    with open(docstring_file_name, 'r') as docstring_file:
        lines = docstring_file.read().split('\n')

    line_max_len = len(max(lines, key=len)) + 1

    docstring = '/* {filler} *\n'.format(filler=line_max_len*'-')
    for line in lines[:-1]:
        docstring += ' * {line} *\n'.format(line=line.ljust(line_max_len))
    docstring += ' * {filler} */\n\n'.format(filler=line_max_len*'-')

    return docstring

if __name__ == "__main__":
    target_file_name = 'bsp.h'
    spec_file_name = 'bsp.csv'
    imports = []
    opts, args = getopt.getopt(sys.argv[1:], ARGSTRING, ARGLIST)
    for opt, arg in opts:
        if opt in ('-i', '--input'):
            spec_file_name = arg
        elif opt in ('-o', '--output'):
            target_file_name = arg
        elif opt in ('--docstring'):
            HEAD_DOCSTRING = create_docstring(arg)
        elif opt in ('--include'):
            imports = arg.split(' ')

    spec_entries = specification_file_read(spec_file_name)
    bsp_file_write(target_file_name, imports, spec_entries)

    print("Specification in {source} written to {target}!".format(source=spec_file_name,
                                                                  target=target_file_name))
