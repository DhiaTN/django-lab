import os
from os.path import dirname
from getpass import getuser

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import _wrappers as wr


DATABASES = settings.DATABASES
PG_VERSION = settings.PG_VERSION
CFG_FILE = settings.DB_SERVER_CFG_FILE

class Command(BaseCommand):
    help = 'Check if the required postgres version is installed'
    __version = None
    __db_user = DATABASES['default']['USER']
    __db_name = DATABASES['default']['NAME']
    __db_password = DATABASES['default']['PASSWORD']
    __server_ip = DATABASES['default']['HOST']

    def add_arguments(self, parser):

        parser.add_argument('-f', '--file', dest='config',
                            default=CFG_FILE, help='File containing server credentials')
        parser.add_argument('-H', '--host', dest='server_ip',
                            default=self.__server_ip, help='IPv4 address of DB server')
        parser.add_argument('-U', '--user', dest='user',
                            default=getuser(), help="Login name of the server's user")
        parser.add_argument('-P', '--password', dest='password',
                            help="Password of the server's user")
        parser.add_argument('-d', '--drop', dest='drop',
                            default=True, help="Drop the old cluster")
        parser.add_argument('-b', '--backup', dest='backup',
                            default=False, help="backup old DB")

    def handle(self, *args, **options):
        if options.get('server_ip') and options.get('user') and options.get('password'):
            config_data = options
        elif options.get('config'):
            config_data = wr.read_server_config(options.get('config'))
        else:
            raise CommandError("Server credentials is required")
        wr.set_server_config(config_data)
        self.__version = wr.pg_version()
        if self.__version:
            if self.__version < PG_VERSION:
                self.output("PostgreSQL {0} detected. Required {1}.".format(
                    self.__version, PG_VERSION), style="error")
                if options.get('backup'):
                    wr.backup_db(self.__db_name, self.__db_user,
                                 self.__db_password, self.__server_ip)
                wr.set_pgcluster_port(self.__version, int(
                    DATABASES['default']['PORT']) + 1)

            else:
                pass

        self.output("Setting up PostgreSQL {0} ...".format(
            PG_VERSION), style="success")
        if self.__version and options.get('drop'):
            wr.pg_dropcluster(self.__version)
            wr.upgrade_pg_pkg(self.__version, PG_VERSION)
        else:
            wr.install_pg_pkg()

        self.output("PostgreSQL {0} successfully installed.".format(
            PG_VERSION), style="success")
        wr.set_pgcluster_port(PG_VERSION, DATABASES['default']['PORT'])
        if self.__version and options.get('backup'):
            wr.restore_db(self.__db_name, self.__db_user,
                          self.__db_password, self.__server_ip)
        else:
            wr.setup_db(self.__db_name, self.__db_user, self.__db_password)
            wr.set_connection_parameter(self.__db_user)
        self.output("{db} is ready.".format(
            db=self.__db_name), style="success")
        wr.pg_ctl('restart', PG_VERSION)

    def output(self, message, style):
        style = getattr(self.style, style.upper())
        self.stdout.write(style(message))
