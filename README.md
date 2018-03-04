# symrepl

`symrepl` is a small utility that helps you investigate the type information inside binaries. It uses `lldb` in order to access the symbolic information inside a binary.

The main use case of this little helper tool is to help vulnerability researchers find interesting things to use while exploiting software.

## Example
The following example shows the loading of the `XUL` binary and how `symrepl` can be used to inspect the internals of the types used inside the binary.

[![asciicast](https://asciinema.org/a/p5G9M4AFcnPzDrEhuzCSMWtKy.png)](https://asciinema.org/a/p5G9M4AFcnPzDrEhuzCSMWtKy)

## Caveats

The script works only on `macOS` so far because this is the platform I'm currently using. A version that supports `linux` or other operating systems that have `lldb` available may or may not be in the works.

## Installation

```
# Install `pip` if not installed.
$ easy_install pip

# Install `virtualenv` if not installed.
$ pip install virtualenv

# Create a virtual python environment.
$ virtualenv venv_symrepl

# Activate the environment (POSIX system).
$ source ./venv_symrepl/bin/activate

# Install `symrepl` into the virtual environment.
$ python setup.py install
```

### Dependencies
All the python requirements will be installed automatically using python's `setuptools`.

- `XCode`
- `python`
- `pip`
- `virtualenv (optional)`

## Usage

Execute `symrepl` with `-h` to get help:

```
$ symrepl -h                                                                                                      usage: symrepl [-h] [-f FILENAME]

Symbol REPL.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --file FILENAME
                        Path to the file with symbol.
```