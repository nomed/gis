"""
Gis Tgext

gearbox gis-sync-mc command integrate MailChimp API

"""
from gearbox.command import Command
import argparse
import sys, os, logging
from paste.deploy import loadapp

log = logging.getLogger('gis.commands.sync')

from gis.lib.mailchimpsync import GisChimpSync
import transaction
class GisSyncCommand(Command):
    """
    """
    def get_description(self):
        return '''Sync With MailChimp'''

    def get_parser(self, prog_name):
        parser = super(GisSyncCommand, self).get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter

        parser.add_argument("-c", "--config",
            help='application config file to read (default: development.ini)',
            dest='config_file', default="development.ini")

        subparser = parser.add_subparsers(dest='command')

        list_parser = subparser.add_parser('list', add_help=False)
        #create_parser.add_argument('name')

        test_parser = subparser.add_parser('test', add_help=False)

        return parser

    def take_action(self, opts):

        config_file = opts.config_file
        config_name = 'config:%s' % config_file
        here_dir = os.getcwd()
        locs = dict(__name__="tgshell")

        # Load locals and populate with objects for use in shell
        sys.path.insert(0, here_dir)

        # Load the wsgi app first so that everything is initialized right
        self.wsgiapp = loadapp(config_name, relative_to=here_dir)

        exec ('import tg') in locs
        exec ('from tg import app_globals, config, request, response, '
              'session, tmpl_context, url') in locs
        locs.pop('__builtins__', None)

        command = getattr(self, 'command_%s' % opts.command)
        command(locs['config'], opts)

    def command_list(self, config, opts):

        gsync = GisChimpSync(config)
        gsync.list()
        transaction.commit()
