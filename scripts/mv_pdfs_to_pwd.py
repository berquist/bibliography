#!/usr/bin/env python3

# originally written on 2015-08-02

from __future__ import print_function

from itertools import count
from itertools import zip_longest

from copy import deepcopy

import os
import shutil


def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def getargs():
    """Get command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('bibfile',
                        help="""The name of the BibTeX file to read in.""")

    parser.add_argument('--file-action',
                        default=None,
                        choices=('copy', 'move'),
                        help="""...""")

    parser.add_argument('--debug',
                        action='store_true',
                        help="""Print lots of stuff to the screen.""")

    args = parser.parse_args()

    return args


def function_does_nothing(*args, **kwargs):
    pass


if __name__ == '__main__':

    import bibtexparser

    args = getargs()

    cwd = os.getcwd()
    if args.file_action == 'copy':
        file_action = shutil.copy2
    elif args.file_action == 'move':
        file_action = function_does_nothing
    else:
        file_action = function_does_nothing

    bibfilename = args.bibfile

    with open(bibfilename) as bibfile:
        old_bibtex_str = bibfile.read()

    old_bib_database = bibtexparser.loads(old_bibtex_str)
    new_bib_database = deepcopy(old_bib_database)

    for entry in old_bib_database.entries:
        entry_file = entry.get('file', None)
        entry_local_url = entry.get('local-url', None)
        # files are separated by semicolons; more than one entry
        # corresponds to supplemental information, whihc may or may
        # not be PDFs
        if entry_file:
            counter = count(start=1)
            split_entry_file = entry_file.split(';')
            # filename components are separated by colons
            # 1. basename
            # 2. absolute path
            # 3. MIME type
            for filename in split_entry_file:
                entry_components = filename.split(':')
                basename, abspath, mime = entry_components
                abspath_dir = os.path.dirname(abspath)
                # No matter what file action we take, check to make
                # sure there isn't going to be a name conflict.
                if os.path.isfile(os.path.join(cwd, basename)):
                    # Need to make sure the new filename we create is
                    # unique.
                    split = os.path.splitext(basename)
                    basename = split[0] + '_{}' + split[1]
                    print(basename)
                    abspath
                file_action(abspath, cwd)

    # new_bibtex_str = bibtexparser.dumps(new_bib_database)
    # print(new_bibtex_str)
