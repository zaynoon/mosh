#!/bin/sh

#
# OS X and Xcode support script.
#

#
# Describe the OS X and Xcode installation, patches, etc as best as possible.
#
describe()
{
    printf "OS X packages:\n"
    pkgutil --pkgs
    printf "Xcode version:\n"
    xcodebuild -version
    printf "Xcode path:\n"
    xcode-select --print-path
    # System Profiler's XML can be read more easily with plutil -p, or
    # saved with an .spx extension and opend with the System Profiler
    # GUI.
    printf "System Profiler:\n"
    system_profiler -xml 2>/dev/null
    printf "OS X report end.\n"
}

#
# Do something.
#
set -e
"$@"
