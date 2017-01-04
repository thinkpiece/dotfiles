#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from optparse import OptionParser
import json
import codecs
import tempfile
import shutil


def deploy_dialog(message, answers):
    answer_list = ' [' + '/'.join(answers) + ']'
    while True:
        answer = input(message + ' ' + answer_list + '? ').strip()
        if answer in answer:
            return answer


def deploy_dotfile(dotfile, options):
    source = ''
    encoding = dotfile.get('encoding', 'utf8')
    temp_path = None
    with codecs.open(dotfile['source'], 'r', encoding='utf8') as srcfile:
        source = srcfile.read()
    with tempfile.NamedTemporaryFile(prefix='dotfiles-', delete=False) as temp:
        temp_path = temp.name
        encoded_writer = codecs.getwriter(encoding)
        temp_writer = encoded_writer(temp)
        temp_writer.write(source)

    skip = False

    if os.path.isfile(dotfile['destination']):
        if options.force:
            print("Overwrite {0}?".format(dotfile['destination']))
        else:
            answer = deploy_dialog("Overwrite the existing {0}".format(
                        dotfile['destination']), ('y', 'n'))
            skip = (answer == 'n')

    if not skip and not options.dryrun:
        print("Writing to {0}...".format(dotfile['destination']))
        if not os.path.isdir(os.path.dirname(dotfile['destination'])):
            os.makedirs(os.path.dirname(dotfile['destination']))
        shutil.copyfile(temp_path, dotfile['destination'])

    if options.dryrun:
        print("The following content will be written to {0}:".format(
              dotfile['destination']))
        with open(temp_path, 'r') as fin:
            print fin.read()

    os.unlink(temp_path)


def get_platform():
    if sys.platform.startswith('linux'):
        return 'linux'
    if sys.platform.startswith('darwin'):
        return 'osx'
    return 'others'

if __name__ == '__main__':
    HOME_DIR = os.path.expanduser('~')
    PLATFORM = get_platform()

    # handling options
    opt_parser = OptionParser()
    opt_parser.add_option('-f', '--force', dest='force',
                          action='store_true', default=False,
                          help="Do not ask even if the file already exist.")
    opt_parser.add_option('-d', '--dryrun', dest='dryrun',
                          action='store_true', default=False,
                          help="No file will be written, instead be shown.")
    opt_parser.add_option('-?', '--home', dest='home_path',
                          type='string', default=HOME_DIR,
                          help="Specify the home directory.")
    opt_parser.add_option(-'p', '--platform', dest='platform',
                          type='string', default=PLATFORM,
                          help="Specify the platform.")
    (options, args) = opt_parser.parse_args()

    with open('preferences.json', 'r') as fp:
        preferences = json.load(fp, encoding='utf-8')

    # option validation
    dotfiles = []

    for filename, data in preferences['dotfiles'].items():
        if PLATFORM not in data['compatible_platforms']:
            continue
        data = data.copy()
        # TODO: use exapndvars() to support the environmental variables
        file_with_path = os.path.join(options.home_path,
                                      data['platform_path'].get(PLATFORM, ''),
                                      filename)
        data['destination'] = file_with_path
        dotfiles.append(data)

    try:
        for dotfile in dotfiles:
            deploy_dotfile(dotfile, options)
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
