from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager
import datetime, os

try:
    from settings_local import *
except ImportError:
    pass

WS1 = WS + ':22'

env.roledefs = {
    'web':         [ WS1,
                   ],
    'db':          [ WS1,
                   ],
}

all_hosts = [WS1,]

new_hosts = []

env.key_filename = [ 'django.pem' ]
env.activate = 'source /home/ubuntu/gemsofcl/venv/bin/activate'
env.directory = '/home/ubuntu/gemsofcl'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

@hosts(env.roledefs['db'])
def deploy_db():
    with virtualenv():
        run("ssh-agent bash -c 'ssh-add /home/ubuntu/.ssh/id_rsa; git pull %s'" % GIT_URL)
        run('./manage.py migrate')

@hosts(env.roledefs['web'])
def deploy_web():
    with virtualenv():
        run("ssh-agent bash -c 'ssh-add /home/ubuntu/.ssh/id_rsa; git pull %s'" % GIT_URL)
        run("ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill -9")

@hosts(env.roledefs['db'])
def get_db():
    sql_file = 'dump_%s.sql' % datetime.datetime.now().strftime('%Y-%m-%d')
    run('mysqldump -u root -p gemsofcl > %s' % sql_file)
    run('tar cvzf dump.tgz %s' % sql_file)
    run('rm %s' % sql_file)
    local('scp -i django.pem %s:/home/ubuntu/dump.tgz .' % WS)

def load_db():
    local('tar xvzf dump.tgz')
    files = os.listdir(os.path.abspath('.'))
    files = filter(lambda x: not os.path.isdir(x), files)
    files = filter(lambda x: '.sql' in x, files)
    newest = max(files, key=lambda x: os.stat(x).st_mtime)
    local('/usr/local/mysql/bin/mysql -u root gemsofcl < %s' % newest)

def deploy():
    execute('deploy_db', roles=['db'])
    execute('deploy_web', roles=['web'])