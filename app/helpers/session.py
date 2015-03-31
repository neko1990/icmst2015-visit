import web

from config import db
from app.models import users

def add_sessions_to_app(app):
    if web.config.get('_session') is None:
        session_store =  web.session.DBStore(db,'sessions')
        session = web.session.Session(app,session_store,initializer={'privilege':0})
        web.config._session = session
    else:
        session = web.config._session

def get_session():
    return web.config._session

def get_user_id():
    return get_session().uid

def login(email):
    s = get_session()
    user = users.get_user_by_email(email)
    for k, v in user.items():
        s[k] = v
    if user.privilege == 1:
        s['actions'] = []
    elif user.privilege == 5:
        s['actions']=[
            ["/AddArticle","Add Article"],
            ["/DelArticle","Del Article"],
            ["/AlterArticle","Alter Article"],
            ["/ResetUserPassword","ResetUserPwd"],
            ["/UserManage","User Management"]
        ]
    s['actions'] += [["/ResetPassword","Reset Password"],["/Profile","Profile"],["/Logout","Logout"]]

def logout():
    s = get_session()
    s.privilege = 0
    s.kill()

def login_required(meth):
    def new(*args,**kw):
        if not get_session().privilege > 0:
            raise web.seeother('/Login')
        return meth(*args,**kw)
    return new

def privilege_match(allowed):
    def _1(func):
        def _2(*args,**kw):
            _p = get_session().privilege
            if isinstance(allowed,list):
                if _p not in allowed:
                    raise web.seeother('/Login')
            elif _p != allowed:
                raise web.seeother('/Login')
            return func(*args,**kw)
        return _2
    return _1
