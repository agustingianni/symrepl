#!/usr/bin/env python

import os
import sys
import argparse
import subprocess

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from pygments import highlight
from pygments.lexers.c_cpp import CppLexer as Lexer
from pygments.formatters import Terminal256Formatter as Formatter

try:
    # macOS: Get the path to lldb's python bindings.
    developer = subprocess.check_output(["xcode-select", "-p"])
    xcode = os.path.split(developer)[0]
    bindings = os.path.join(xcode, "SharedFrameworks/LLDB.framework/Resources/Python")
    sys.path.append(bindings)
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

        if query == "quit":
            break

        # Query the DB.
        found_types = symrpl.getTypes(query)
        if not len(found_types):
            print "Could not find any types that match `{}`".format(query)
            continue

        # Display each type that matches.
        print "Found {} types matching `{}`".format(len(found_types), query)
        for output in found_types:
            print highlight(output, Lexer(), Formatter())
            print


def main():
    parser = argparse.ArgumentParser(description='Symbol REPL.')
    parser.add_argument('-f', '--file', dest='filename',
                        action='store', help='Path to the file with symbol.')

    args = parser.parse_args()
    if not args.filename:
        parser.print_help()
        sys.exit(-1)

    try:
        repl_loop(args.filename)

    except (EOFError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
