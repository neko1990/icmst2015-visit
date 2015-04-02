import web
import os
from web.contrib.template import render_jinja

DB_NAME = 'db.sqlite3'
db = web.database(dbn='sqlite',db=DB_NAME)
db.printing = False

upload_dir = "./receive/"

web.config.debug = True

# used to save password
PASSWORD_SALT = "jlk38blksdivnsfFoNsAlT754-"

# session parameters
web.config.session_parameters.cookie_name = "visiticm_sid"
web.config.session_parameters.secret_key = 'session--saltvisiticm'

# template cache
cache = False

# static page path
STATIC_PATH = os.path.realpath('static')

# view
render = render_jinja(
    'app/templates',
    encoding = 'utf-8')

render._lookup.globals.update({
    'session_getter':(lambda : web.config._session),
    'title_list_getter':(lambda : web.config._title_list)})

# TODO how to set this?
web.config.email_errors = ''

PROFILE_LINKS = [
    ["/Profile","Profile"],
    ["/ResetPassword","Reset Password"]
]

PROPERTY_LIST = ['email']
