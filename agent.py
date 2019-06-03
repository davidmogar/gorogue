#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import random
import string
import subprocess

AGENT_PREFFIXES = ('agent-', 'rogue-')

parser = argparse.ArgumentParser(description='Run a dockerized Puppet agent')
parser.add_argument('--docker-cli',
                    default='docker',
                    help='Docker command to use (default: %(default)s)')
parser.add_argument('--docker-image',
                    default='puppet/puppet-agent',
                    help='Docker image to use (default: %(default)s)')
parser.add_argument('--docker-link',
                    default='puppet:puppet',
                    help='Docker container to link to (default: %(default)s)')
parser.add_argument('--go-rogue',
                    action='store_true',
                    help='Run Puppet against a compromised Puppet code')
parser.add_argument('--no-rm',
                    action='store_false',
                    help='Do not delete container once exited')
args = parser.parse_args()


def generate_docker_command(hostname):
    command = [
        args.docker_cli,
        'run',
        '--hostname', hostname,
        '--link', args.docker_link,
        args.docker_image
    ]

    if args.no_rm:
        command.insert(-1, '--rm')

    return command


def generate_name(length=13):
    return (AGENT_PREFFIXES[1 if args.go_rogue else 0] +
                ''.join(random.choice(string.ascii_lowercase) for i in range(length)))


def run_docker(hostname):
    command = generate_docker_command(hostname)

    try:
        with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
            for line in process.stdout:
                print(line.rstrip().decode())
    except Exception as error:
        print('Error while running command:', error)


if __name__ == "__main__":
    if args.go_rogue:
        print('\U0001F608\tGoing rogue')

    hostname = generate_name()

    print("\U0001F64B\tHello, I'm", hostname)
    input('\U0001F40B\tPress Enter to run the container...')

    run_docker(hostname)