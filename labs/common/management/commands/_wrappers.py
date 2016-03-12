import os
import re
import json
from sys import argv
from getpass import getuser
from fabric.api import env, sudo, run, cd, local


PKG_SOURCE_FILE = '/etc/apt/sources.list'
PG_APT = 'deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main'
PG_APT_KEY = 'https://www.postgresql.org/media/keys/ACCC4CF8.asc'
PGCONF_FILE = '/etc/postgresql/{v}/main/postgresql.conf'
BACKUP_PATH = '/tmp'


def apt_update():
    sudo('apt-get update')


def apt(cmd, *pakages):
    pakages = ' '.join(pakages)
    sudo('apt-get {cmd} {pkgs}'.format(cmd=cmd, pkgs=pakages))


def apt_autoremove():
    sudo('apt-get autoremove')


def read_server_config(filepath='server.cfg'):
    with open(filepath) as data:
        return json.loads(data.read())


def set_server_config(data):
    env.host_string = data.get('server_ip', '127.0.0.1')
    env.user = data.get('user', getuser())
    env.password = data.get('password', '')


def pg_ctl(action, version=''):
    actions = ['start', 'stop', 'restart', 'status', 'reload', 'force-reload']
    if action not in actions:
        raise ValueError('Expected actions: {0}'.format(actions))
    sudo('/etc/init.d/postgresql {0} {1}'.format(action, version))


def psql(sql_command):
    if sql_command.endswith(';'):
        sql_command = sql_command.rstrip(";")
    sudo('sudo -u postgres psql -c "{cmd};"'.format(cmd=sql_command))


def set_pgcluster_port(version, port=5432):
    pattern = 's/port = [0-9]*/port = {port}/g'.format(port=port)
    cfg_file = PGCONF_FILE.format(v=version)
    sudo("sed -ie '{regex}' {cfg}".format(regex=pattern, cfg=cfg_file))


def pg_version():
    try:
        output = run('psql --version')
        pattern = re.compile(r'(\d+\.)(\d+)')
        result = pattern.search(output)
        return result.group()
    except SystemExit as e:
        return None


def install_pg_pkg(version):
    pkgs = 'postgresql-{0} postgresql-client-{0} postgresql-contrib-{0} postgresql-server-dev-{0}'
    sudo('echo "{apt}" >> {file}'.format(apt=PG_APT, file=PKG_SOURCE_FILE))
    sudo('wget -q -O - {url} | sudo apt-key add -'.format(url=PG_APT_KEY))
    apt('update')
    apt('install', 'libpq-dev')
    apt('install', pkgs.format(version))
    apt('autoremove')


def upgrade_pg_pkg(_from, _to):
    pkgs = 'postgresql-{0} postgresql-client-{0} postgresql-contrib-{0} postgresql-server-dev-{0}'
    apt('--purge remove', pkgs.format(_from))
    apt('autoremove')
    install_pg_pkg(_to)


def setup_db(db_name, db_user, password):
    psql('CREATE DATABASE {db}'.format(db=db_name))
    psql('CREATE USER {u} WITH PASSWORD \'{p}\''.format(u=db_user, p=password))
    psql('GRANT ALL PRIVILEGES ON DATABASE {db} TO {u}'.format(
        db=db_name, u=db_user))
    set_connection_parameter(db_user=db_user)


def set_connection_parameter(db_user, **settings):
    if not settings:
        settings = {
            'client_encoding': 'utf8',
            'default_transaction_isolation': 'read committed',
            'timezone': 'UTC'
        }
    for p, v in settings.items():
        psql("ALTER ROLE {u} SET {p} TO '{v}'".format(p=p, v=v, u=db_user))


def backup_db(db_name, db_user, password, db_server=env.host_string):
    with cd('/tmp'):
        local('pg_dump -U {user} -h {ip} {db} > {db}-bak.sql'.format(
            user=db_user,
            ip=db_server,
            pwd=password,
            db=db_name
        ))


def restore_db(db_name, db_user, password, db_server=env.host_string):
    local('psql -U {user} -h {ip} {db} < /tmp/{db}-bak.sql'.format(
        user=db_user,
        ip=db_server,
        pwd=password,
        db=db_name
    ))


def pg_dropcluster(pg_version):
    sudo("pg_dropcluster --stop {v} main".format(v=pg_version))
