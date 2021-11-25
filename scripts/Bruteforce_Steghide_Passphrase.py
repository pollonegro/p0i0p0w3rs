#!/usr/bin/python3
# Author: https;//github.com/cOb4l7
# Description: A script to brute-force steghide passphrase.
# Dependecies: steghide

import argparse
import subprocess
import os

from threading import Thread


def steghideCracker(password, stegofile):
    """
    Brute-Force steghide passphrase

    This function brute-force steghide passphrase using a given file.

    Parameters
    ----------
        password: The passphrase
        stegofile: Selected stego file

    """
    steghide = ["steghide", "extract", "-sf", stegofile, "-p", password]

    FNULL = open(os.devnull, 'w')

    status = subprocess.run(args=steghide, stdout=FNULL,
                            stderr=subprocess.STDOUT)

    if status.returncode != 1:
        print("\033[32mSuccessfully brute-foce \033[35m{0}\033[32m passphrase:\
              \033[36m{1}\033[0m".format(stegofile, password))
        os._exit(0)


def main():
    parse = argparse.ArgumentParser(usage='%(prog)s [options]',
                                    description="A simple program to brute-\
                                    force steghide passhrase",
                                    epilog="Happy hacking ;)")
    parse.add_argument('-d', '--dictionary', help='Specify a dictionary file',
                       required=True, metavar='', dest='passfile',
                       type=argparse.FileType('r', encoding='latin-1'))
    parse.add_argument('-sf', '--stegofile', help='Specify a stego file',
                       required=True, metavar='', dest='stegofile')

    options = parse.parse_args()

    dict_file = options.passfile.read().splitlines()
    stegofile = options.stegofile

    for password in dict_file:
        t = Thread(target=steghideCracker, args=(password, stegofile))
        t.start()



if __name__ == "__main__":
    main()
