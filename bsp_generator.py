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
                  " * This an automatic generated file.            *\n"
                  " * Do not alter it, change the specification csv*\n"
                  " * instead.                                     *\n"
                  " * -------------------------------------------- */\n"
                  "\n")


def specification_file_read(spec_file_name):
    entries = []

    with open(spec_file_name, 'r') as spec_file:
        csvreader = csv.DictReader(spec_file, delimiter=',', quotechar='"')
        for row in csvreader:
            entries.append(row)

    return entries


def build_line(entry):
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


def build_module_seperator(module, submodule):
    line = '\n// Defines for {}'.format(module)
    if submodule:
        line += '-> {}'.format(submodule)
    line += '\n'
    return line


def build_import_header(imports):
    header = ''
    for lib in imports:
        header += '#include <{}.h>\n'.format(lib)
    header += '\n'
    return header


def bsp_file_write(bsp_file_name, imports, entries):
    with open(bsp_file_name, 'w') as bsp_file:
        current_module = ''
        current_submodule = ''

        bsp_file.write(HEAD_INCLUDE_GUARD)
        bsp_file.write(HEAD_DOCSTRING)
        bsp_file.write(build_import_header(imports))

        for entry in entries:
            if current_module != entry['Module'] or \
               current_submodule != entry['Submodule']:
                current_module = entry['Module']
                bsp_file.write(build_module_seperator(entry['Module'],
                                                      entry['Submodule']))
            bsp_file.write(build_line(entry))

        bsp_file.write(BOT_INCLUDE_GUARD)

if __name__ == "__main__":
    target_file_name = 'bsp.h'
    spec_file_name = 'bsp.csv'
    imports = ['stdint', 'stm32f411_gpio']

    opts, args = getopt.getopt(sys.argv[1:], 'i:o:', ['input=', 'output='])
    for opt, arg in opts:
        if opt in ('-i', '--input'):
            spec_file_name = arg
        elif opt in ('-o', '--output'):
            target_file_name = arg

    spec_entries = specification_file_read(spec_file_name)
    bsp_file_write(target_file_name, imports, spec_entries)

    print("Specification in {source} written to {target}!".format(source=spec_file_name,
                                                                  target=target_file_name))
