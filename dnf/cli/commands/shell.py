# shell.py
# Shell CLI command.
#
# Copyright (C) 2016 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from dnf.cli import commands
from dnf.i18n import _


import dnf
import logging
import shlex
import sys


logger = logging.getLogger('dnf')


class ShellCommand(commands.Command):

    aliases = ('shell',)
    summary = _('')

    MAPPING = {'repo': 'repo',
               'repository': 'repo',
               'exit': 'quit',
               'quit': 'quit',
               'run': 'run_ts',
               'ts': 'transaction',
               'transaction': 'transaction',
               'config': 'config'}

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('script', nargs='?', metavar=_('SCRIPT'),
                            help=_('Script to run in DNF shell'))

    def configure(self):
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True
        demands.resolving = False
        demands.root_user = True

    def run(self):
        while True:
            line = dnf.i18n.ucd_input('> ')
            s_line = shlex.split(line)
            opts = self.cli.optparser.parse_main_args(s_line)
            if opts.command in self.MAPPING:
                getattr(self, '_' + self.MAPPING[opts.command])()
            else:
                cmd_cls = self.cli.cli_commands.get(opts.command)
                if cmd_cls is not None:
                    cmd = cmd_cls(self)
                    opts = self.cli.optparser.parse_command_args(cmd, s_line)
                    cmd.run()

    def _config(self):
        pass

    def _repo(self):
        pass

    def _run_ts(self):
        pass

    def _transaction(self):
        pass

    def _quit(self):
        pass