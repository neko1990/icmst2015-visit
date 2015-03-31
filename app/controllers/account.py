import web
from web import form
from web import Storage

from app.models import users

from app.helpers import session
from app.helpers import utils
from app.helpers import mywebwidgets as mww

from app.helpers.forms import login_form
from app.helpers.forms import register_detail_form
from app.helpers.forms import reset_password_form
from app.helpers.forms import register_form
from app.helpers.forms import forgot_password_form

from config import PROPERTY_LIST
from config import render

class Register:
    def GET(self):
        if session.get_session().privilege != 0:
            # already login
            raise web.seeother('/Profile')
        form = mww.MyForm(register_form(),'/Register')
        r = mww.Panel('Register',form.render_css()).render()
        return render.l12(r)

    def POST(self):
        f = mww.MyForm(register_form(),'/Register')
        ipt = web.input(_unicode=False)
        if not f.form.validates(ipt):
            show = web.input(show='all').show
            r = mww.Panel('Register',f.render_css()).render()
            return render.l12(r)
        else:
            users.create_account(
                email = f.form.d.email,
                password = f.form.d.password,
                privilege = 1)
            session.login(f.form.d.email)
            raise web.seeother('/SendApply')

class Login:
    def GET(self):
        form = mww.MyForm(login_form(),'/Login')
        r = mww.Panel('Login',form.render_css()).render()
        return render.l12(r)

    def POST(self):
        f = mww.MyForm(login_form(),'/Login')
        ipt = web.input(_unicode=False)
        if not f.form.validates(ipt):
            # show = ipt.get('show','all')
            show = web.input(show='all').show
            r = mww.Panel('Login',f.render_css()).render()
            return render.l12(r)
        else:
            session.login(f.form.d.email)
            raise web.seeother('/SendApply')

class Logout:
    def GET(self):
        session.logout()
        raise web.seeother('/')

class Profile:
    @session.login_required
    def GET(self):
        f = mww.MyForm(register_detail_form(),'/Profile')
        f.form.fill(utils.extract_info_from_storage_by_list(session.get_session(),PROPERTY_LIST))
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Profile',f.render_css())
        return render.l3r9(l.render(),r.render())

    @session.login_required
    def POST(self):
        ipt = web.input(_unicode=True)
        f = mww.MyForm(register_detail_form(),'/Profile')
        if not f.form.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Profile',f.render_css())
            return render.l3r9(l.render(),r.render())
        else:
            users.update(session.get_session().uid,
                         **utils.extract_info_from_storage_by_list(ipt,PROPERTY_LIST))
            session.login(session.get_session().email)
            return "success"

class ResetPassword:
    @session.login_required
    def GET(self):
        f = mww.MyForm(reset_password_form(),'/ResetPassword')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Reset Password',f.render_css())
        return render.l3r9(l.render(),r.render())

    @session.login_required
    def POST(self):
        ipt = web.input(_unicode=True)
        f = reset_password_form()
        if not f.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Reset Password',f.render_css())
            return render.l3r9(l.render(),r.render())
        else:
            users.reset_password(session.get_session().uid,ipt.new_password)
            return "success"

class ResendPassword:
    # TODO ResendPassword
    @session.login_required
    def GET(self):
        return 'Hello, resend !! this is not implement, should config your mail server first !!'
