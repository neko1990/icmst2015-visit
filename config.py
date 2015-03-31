import web
import os

DB_NAME = 'db.sqlite3'
db = web.database(dbn='sqlite',db=DB_NAME)

upload_dir = "./receive/"

web.config.debug = False

# used to save password
PASSWORD_SALT = "jlk38b2WSA2fFoNsAlT754-"

# session parameters
web.config.session_parameters.cookie_name = "icmst2015_sid"
web.config.session_parameters.secret_key = 'session--salt'

# template cache
cache = False

# static page path
STATIC_PATH = os.path.realpath('static')

# render or view
render = web.template.render(
    'app/templates',base="base",cache=cache,
    globals={
        'context': (lambda : web.config._session),
        'title_list':(lambda : web.config._title_list)
    })

# mail setting
web.config.smtp_server = 'mail.cumt.edu.cn'
web.config.smtp_username = 'icmst2015'
web.config.smtp_password = '664df778bdf272fe'
web.config.smtp_starttls = True

# TODO how to set this?
web.config.email_errors = ''

COUNTRY_LIST = [
'mining','computer'
]

PROFILE_LINKS = [
    ["/Profile","Profile"],
    ["/ResetPassword","Reset Password"]
]

PROPERTY_LIST = ['email']

