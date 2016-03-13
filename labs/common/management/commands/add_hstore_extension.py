from getpass import getuser

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import _wrappers as wr


CFG_FILE = settings.DB_SERVER_CFG_FILE
SERVER_IP = settings.DATABASES['default']['HOST']
DB_USER = settings.DATABASES['default']['USER']

class Command(BaseCommand):
    help = 'Setup the hstore extension in PostgreSQL'

    def add_arguments(self, parser):

        parser.add_argument('-f', '--file', dest='config',
                            default=CFG_FILE, help='File containing server credentials')
        parser.add_argument('-H', '--host', dest='server_ip',
                            default=SERVER_IP, help='IPv4 address of DB server')
        parser.add_argument('-U', '--user', dest='user',
                            default=getuser(), help="Login name of the server's user")
        parser.add_argument('-P', '--password', dest='password',
                            help="Password of the server's user")

    def handle(self, *args, **options):
        if options.get('server_ip') and options.get('user') and options.get('password'):
            config_data = options
        elif options.get('config'):
            config_data = wr.read_server_config(options.get('config'))
        else:
            raise CommandError("Server credentials are wrong or missing")
        wr.set_server_config(config_data)
        wr.upgrade_to_superuser(DB_USER)
        wr.create_hstore_extenstion()
        self.output("HStore extension successfully created.", style="success")

    def output(self, message, style):
        style = getattr(self.style, style.upper())
        self.stdout.write(style(message))
