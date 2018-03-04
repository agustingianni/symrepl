#!/usr/bin/env python

import argparse
import os
import platform
import subprocess
import sys

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from pygments import highlight
from pygments.lexers.c_cpp import CppLexer as Lexer
from pygments.formatters import Terminal256Formatter as Formatter

try:
    if platform.system() == 'Darwin':
        # macOS: Get the path to lldb's python bindings.
        developer = subprocess.check_output(['xcode-select', '-p'])
        xcode = os.path.split(developer)[0]
        bindings = os.path.join(xcode, 'SharedFrameworks', 'LLDB.framework', 'Resources', 'Python')
        sys.path.append(bindings)
    elif platform.system() == 'Linux':
        # 'lldb --python-path' should spit out the lldb python path, but this broken (?)
        # on linux. So we'll add it to our path anyways, incase its just my box that its
        # broken on...
        lldb_python_path = subprocess.check_output(['lldb', '--python-path']).strip()
        sys.path.append(lldb_python_path)

        # this is where the shit actually lives on my debian box. Introduces a dep on 'llvm-config'
        # but also like, works and stuff.
        llvm_lib_dir = subprocess.check_output(['llvm-config', '--libdir']).strip()
        llvm_python_path = os.path.join(llvm_lib_dir, 'python2.7', 'site-packages')
        lldb_python_path = os.path.join(llvm_python_path, 'lldb')

        sys.path.append(llvm_python_path)
        sys.path.append(lldb_python_path)
    else:
        print 'Failed determining platform, attempting to import lldb anyways...'

    import lldb

except Exception, e:
    print "Failed importing lldb's python bindings."
    sys.exit(-1)


class SYMRepl(object):
    def __init__(self, filename):
        # Create a debugger.
        self.debugger = lldb.SBDebugger.Create()
        self.debugger.SetAsync(False)

        architecture = lldb.LLDB_ARCH_DEFAULT
        target = self.debugger.CreateTargetWithFileAndArch(
            filename, architecture)
        if not target:
            sys.exit(-1)

        self.module = target.GetModuleAtIndex(0)
        if not self.module:
            sys.exit(-1)

    def getTypes(self, type_name):
        types = self.module.FindTypes(type_name)
        if not types.GetSize():
            return []

        return map(str, types)


def repl_loop(filename):
    # Load the database of symbols.
    symrpl = SYMRepl(filename)

    while 1:
        query = str(prompt(
            u'symrepl> ',
            history=FileHistory('history.txt'),
            auto_suggest=AutoSuggestFromHistory(),
            lexer=Lexer,
        ))

        if query == 'quit':
            break

        # Query the DB.
        found_types = symrpl.getTypes(query)
        if not len(found_types):
            print 'Could not find any types that match `{}`'.format(query)
            continue

        # Display each type that matches.
        print 'Found {} types matching `{}`'.format(len(found_types), query)
        for output in found_types:
            print highlight(output, Lexer(), Formatter())
            print


def main():
    parser = argparse.ArgumentParser(description='Symbol REPL.')
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', help='Path to the file with symbols.')

    args = parser.parse_args()
    if not args.filename:
        parser.print_help()
        sys.exit(-1)

    try:
        repl_loop(args.filename)

    except (EOFError, KeyboardInterrupt):
        pass


if __name__ == '__main__':
    main()
