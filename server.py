#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import platform
import random
import string
import subprocess

AGENT_PREFFIXES = ('agent-', 'rogue-')
PUPPET_SERVER_COMMAND = '/opt/puppetlabs/bin/puppetserver foreground'

parser = argparse.ArgumentParser(description='Run a dockerized Puppet agent')
parser.add_argument('--docker-cli',
                    default='docker',
                    help='Docker command to use (default: %(default)s)')
parser.add_argument('--docker-image',
                    default='puppet/puppetserver-standalone',
                    help='Docker image to use (default: %(default)s)')
parser.add_argument('--docker-name',
                    default='puppet',
                    help='Docker container to link to (default: %(default)s)')
parser.add_argument('--no-rm',
                    action='store_false',
                    help='Do not delete container once exited')
args = parser.parse_args()


def copy_command_to_clipboard():
    clip_command = 'echo "%s" | %s' % (PUPPET_SERVER_COMMAND,
                                     'pbcopy' if platform.system() == 'Darwin' else 'clip')

    return subprocess.call(clip_command, shell=True) == 0


def generate_docker_command():
    repo_path = os.path.dirname(os.path.realpath(__file__))
    module_path = os.path.join(repo_path, 'gorogue-module')
    server_path = os.path.join(repo_path, 'gorogue-server/go_build_main_go_linux')

    command = [
        args.docker_cli,
        'run',
        '-it',
        '-v', '%s:/etc/puppetlabs/code/environments/production/modules/' % module_path,
        '-v', '%s:/gorogue' % server_path,
        '--entrypoint', '/bin/bash',
        '--name', args.docker_name,
        args.docker_image
    ]

    if args.no_rm:
        command.insert(-1, '--rm')

    return command


def run_docker():
    command = generate_docker_command()

    try:
        os.system(' '.join(command))
    except Exception as error:
        print('Error while running command:', error)


if __name__ == "__main__":
    print("\U0001F991\tRun '%s'" % PUPPET_SERVER_COMMAND)

    if copy_command_to_clipboard():
        print('\U0001F4CB\tCommand copied to the clipboard')
    else:
        print('\U0001F926\tCommand not copied to the clipboard')

    input('\U0001F40B\tPress Enter to run the container...')

    run_docker()
