
"""
WEBFACTION_PASSWORD=thepassword fab install
WEBFACTION_PASSWORD=thepassword fab update
"""
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from fabric.contrib.files import upload_template, exists
import os
import sys
from fabric.context_managers import path

print __name__

sys.path.append(os.path.dirname(__name__))


env.config_ok = False

def _common():
    env.user="mkeller"
    env.hosts = [env.user + ".webfactional.com"]
    env.password = os.getenv("WEBFACTION_PASSWORD")
    if not env.password:
        env.password = raw_input("Webfaction password:")
    
    env.wsgi_handler = "wsgi:application"
    env.app_dir = "/home/%s/webapps/%s" % (env.user, env.app_name)
    env.temp_dir = env.app_dir + "/temp"
    env.env_dir = env.app_dir + "/env"
    env.node_dir = env.app_dir + "/nodejs"
    env.conf_dir = env.app_dir + "/conf"
    env.virtualenv = env.app_dir + "/env"
    env.bin_dir = env.app_dir + "/bin"
    env.media_dir = env.app_dir + "/media"
    env.static_dir = env.app_dir + "/collected_static"
    
    env.config_ok = True

def itcm():
    import settings
    env.settings = settings
    env.domain = "itcm-sussex.com"
    env.app_name = "itcq" # Original name was itcq
    env.settings_module = "settings"
    _common()

# Only one site so load its setting by default
vamp()
    
def webfaction_login():
  print "Logging in to webfaction"
  from xmlrpclib import ServerProxy, Error
  wfapi = ServerProxy("https://api.webfaction.com/")
  print env.user
  wf_session_id, _account = wfapi.login(env.user, env.password)
  print "logged in", wf_session_id
  return wfapi, wf_session_id

def add_cronjob(cronline):
    wfapi, wf_session_id = webfaction_login()
    try:
        wfapi.delete_cronjob(wf_session_id, cronline)
    except:
        pass
    wfapi.create_cronjob(wf_session_id, cronline)

def add_restart_cron():
    print "Add restart cron"
    add_cronjob("*/1 * * * * %s/start_supervisor.sh start" % (env.bin_dir,))
    
# def add_notify_cron():
#     command = "%s/bin/python ~/webapps/%s/src/manage.py %s --settings=%s" % (env.virtualenv, env.app_name, "send_notifications" ,env.settings_module)
#     add_cronjob("0 0 * * * %s" % (command,))

def install_webfaction():
    """
    Use the webfaction API to setup the needed apps, websites and
    domains. Should be idempotent so it's fine to run it even when
    it's not needed.
    """
    wfapi, wf_session_id = webfaction_login()
    print "Create domain"
    wfapi.create_domain(wf_session_id, env.domain, "www")
    print "Create apps"
    apps_list = wfapi.list_apps(wf_session_id)
    for name, type, app_settings in [(env.app_name, "custom_app_with_port",""),
                                 (env.app_name + "_static", "symlink_static_only", env.static_dir),
                                 (env.app_name + "_media",  "symlink_static_only", env.media_dir),
                                 (env.app_name + "_supervisor", "custom_app_with_port", "")]:
        app = [x for x in apps_list if x["name"] == name]
        if app:
            print "App", name, "already exists, using it"
        else:
            print "Creating app", name
            wfapi.create_app(wf_session_id, name, type, False, app_settings)
    print "Find IP"
    # Assuming that only have one server and one main ip I want to use
    ip = [x for x in wfapi.list_ips(wf_session_id) if x["is_main"]][0]["ip"]
    print ip
    def setup_website(name, https):
        print "Create website",name
        website_list = wfapi.list_websites(wf_session_id)
        website = [x for x in website_list if x["name"] == name]
        if website:
            print "Website already exists, updating"
            method = wfapi.update_website
        else:
            print "Creating website"
            method = wfapi.create_website
        method(wf_session_id, name, ip, https, ["www." + env.domain, env.domain],
                             (env.app_name, '/'),
                             (env.app_name + "_static", '/static'),
                             (env.app_name + "_media", '/media'))

    setup_website(env.app_name + "_http", False)
    setup_website(env.app_name + "_https", True)
    
    print "Create DB"
    db_list = wfapi.list_dbs(wf_session_id)
    db_name = "%s_%s" % (env.user, env.app_name)
    db = [x for x in db_list if x["name"] == db_name]
    if db:
        print "DB already exists, assuming password and type are correct"
    else:
        wfapi.create_db(wf_session_id, db_name, "postgresql", env.settings.DATABASES["default"]["PASSWORD"])
    print "Set media dir acl"
    wfapi.set_apache_acl(wf_session_id, env.media_dir, "rwx")
    add_restart_cron()
    # add_notify_cron()

    setup_mailbox()
    query_webfaction()

def setup_mailbox():
    wfapi, wf_session_id = webfaction_login()
    try:
        wfapi.create_mailbox(wf_session_id, env.settings.EMAIL_HOST_USER)
    except:
        print "Failed to create mailbox, assume it's already created"
    wfapi.change_mailbox_password(wf_session_id, env.settings.EMAIL_HOST_USER, env.settings.EMAIL_HOST_PASSWORD)

def query_webfaction():
    wfapi, wf_session_id = webfaction_login()
    print "Query webfaction"
    apps = wfapi.list_apps(wf_session_id)
    main_app = [x for x in apps if x["name"] == env.app_name][0]
    supervisor_app = [x for x in apps if env.app_name +  "_supervisor" == x["name"]][0]
    env.server_port = main_app["port"]
    env.supervisor_port = supervisor_app["port"]


def upload():
    rsync_project(local_dir=os.path.dirname(__file__) + "/",
                  remote_dir="~/webapps/%s/src" % (env.app_name,),
                  delete=True, exclude=('*local_settings.py*', 'node_modules',))

def start():
    run("bash %s/start_supervisor.sh start" % (env.bin_dir,))

def stop():
    run("bash %s/start_supervisor.sh stop" % (env.bin_dir,))

def restart():
    run("bash %s/start_supervisor.sh restart" % (env.bin_dir,))

def manage(cmd, options=""):
    with path(env.bin_dir, "prepend"):
        run("%s/bin/python ~/webapps/%s/src/manage.py %s --settings=%s %s" % (env.virtualenv, env.app_name,cmd,env.settings_module, options))

def shell():
    manage("shell")

def taillogs():
    run("tail -f ~/logs/user/%s_django.log" % (env.app_name))

def migratedb():
    manage("syncdb", "--migrate")

def update_supervisord():
    upload_template("conf_templates/supervisord.conf",
                    env.conf_dir + "/supervisord.conf",
                    {
                        "user": env.user,
                        "password": "9u310urfi3", # we're not exposing the port so this isn't so important
                        "supervisor_port": env.supervisor_port,
                        "wsgi_handler": env.wsgi_handler,
                        "port": env.server_port,
                        "app_name": env.app_name,
                        "app_dir": env.app_dir,
                        "bin_dir": env.bin_dir,
                        "conf_dir": env.conf_dir,
                        "virtualenv": env.virtualenv,
                        "settings_module": env.settings_module 
                     })
    upload_template("conf_templates/start_supervisor.sh",
                    env.bin_dir + '/start_supervisor.sh',
                    {
                        "user": env.user,
                        "conf_dir": env.conf_dir,
                        "virtualenv": env.virtualenv,
                        "app_name": env.app_name
                    },
                    mode=0750,
                    )




def updatepackages():
    run("PATH=/usr/pgsql-9.1/bin/:$PATH ~/webapps/%s/env/bin/pip install -r ~/webapps/%s/src/requirements.txt" % (env.app_name, env.app_name))

def updatenpmpackages():
    with cd("~/webapps/%s/src" % (env.app_name,)):
        if not exists("node_modules"):
            run("mkdir node_modules")
        run("%s/npm install" % (env.bin_dir))

# def installredis():
#     run("wget http://redis.googlecode.com/files/redis-2.4.4.tar.gz")
#     run("tar xzf redis-2.4.4.tar.gz")
#     with cd("redis-2.4.4"):
#         run("make")
#         run("cp src/redis-server src/redis-cli %s" %(env.bin_dir,))
#     updateredisconf()

# def updateredisconf():
#    upload_template("conf_templates/redis.conf",
#                    env.conf_dir + "/redis.conf",
#                    {
#                        "port": env.redis_port,
#                        "dir": env.redis_dir
#                    }
#                    )

def collectstatic():
   manage("collectstatic","--noinput")

def update_djstripe():
    manage("djstripe_init_customers")
    manage("djstripe_init_plans")

def bootstrap_virtualenv():
    with cd(env.temp_dir):
        run("curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.tar.gz")
        run("tar xzf virtualenv-1.10.tar.gz")
        run('python2.7 virtualenv-1.10/virtualenv.py %s' % (env.env_dir))
        run("%s/bin/pip install virtualenv-1.10.tar.gz" % (env.env_dir))
        run("rm virtualenv-1.10.tar.gz")
        run("rm -rf virtualenv-1.10")

def installnodejs():
    with cd(env.temp_dir):
        run("curl -O http://nodejs.org/dist/v0.10.26/node-v0.10.26.tar.gz")
        run("tar xzf node-v0.10.26.tar.gz")
        with cd("node-v0.10.26/"):
            run("python2.7 configure --prefix=%s" % (env.node_dir))
            run("make && make install")
            run("ln -s %s/bin/node %s/node" % (env.node_dir, env.bin_dir))
            run("ln -s %s/bin/npm %s/npm" % (env.node_dir, env.bin_dir))

def install():
    if not env.config_ok:
        print "Please specify a site"
        return
    install_webfaction()
    for d in [env.conf_dir, env.bin_dir, env.media_dir, env.temp_dir]:
        if not exists(d):
            run("mkdir " + d)
    if not exists("%s/bin/activate" % (env.env_dir)):
        bootstrap_virtualenv()
    # installredis()
    # if not exists("%s/node" % (env.bin_dir)):
    #     installnodejs()
    update()

def update():
    if not env.config_ok:
        print "Please specify a site"
        return
    query_webfaction()
    upload()
    updatenpmpackages()
    updatepackages()
    migratedb()
    update_djstripe()
    # updateredisconf()
    update_supervisord()
    collectstatic()
    restart()
