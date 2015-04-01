# -*- coding: utf-8 -*-
import web
from web import form
from web import Storage

from app.models import users

from app.helpers import session
from app.helpers import utils
from app.helpers import mywebwidgets as mww

from config import PROPERTY_LIST
from config import render

vemail = form.regexp(r'.+@.+', 'Please enter a valid email address')

class Register:
    def GET(self):
        if session.get_session().privilege != 0:
            # already login
            raise web.seeother('/Profile')
        form = mww.MyForm(self.register_form(),'/Register')
        r = mww.Panel(u'注册',form.render_css()).render()
        return render.l12( page = r)

    def POST(self):
        f = mww.MyForm(self.register_form(),'/Register')
        ipt = web.input(_unicode=False)
        if not f.form.validates(ipt):
            show = web.input(show='all').show
            r = mww.Panel(u'注册',f.render_css()).render()
            return render.l12( page = r)
        else:
            users.create_account(
                email = f.form.d.email,
                password = f.form.d.password,
                privilege = 1)
            session.login(f.form.d.email)
            raise web.seeother('/SendApply')

    def register_form(self):
        return form.Form(
            form.Textbox('email',
                         form.notnull, vemail,
                         form.Validator('This email address is already taken.',
                                        lambda x: users.is_email_available(x)),
                         description=u'* 邮箱 ',
                         class_="form-control"),
            form.Password('password',
                          form.notnull,
                          form.Validator('Password must at least 5 characters long.',
                                         lambda x: users.is_valid_password(x)),
                          description=u'* 密码',
                          class_="form-control"),
            form.Password('re_password',
                          form.notnull,
                          description=u"* 确认密码",
                          class_="form-control"),
            form.Button('Sign Up', type='submit', value='Register' , class_="btn btn-primary"),
            validators = [
                form.Validator('Password Not Match!.', lambda i:i.password == i.re_password)
            ]
        )

class Login:
    def GET(self):
        form = mww.MyForm(self.login_form(),'/Login')
        r = mww.Panel('Login',form.render_css()).render()
        return render.l12( page = r)

    def POST(self):
        f = mww.MyForm(self.login_form(),'/Login')
        ipt = web.input(_unicode=False)
        if not f.form.validates(ipt):
            # show = ipt.get('show','all')
            show = web.input(show='all').show
            r = mww.Panel('Login',f.render_css()).render()
            return render.l12( page = r)
        else:
            session.login(f.form.d.email)
            raise web.seeother('/SendApply')

    def login_form(self):
        return form.Form(
            form.Textbox('email',
                         form.notnull, vemail,
                         description=u'邮箱',
                         class_="form-control"),
            form.Password('password',
                          form.notnull,
                          description=u'密码',
                          class_="form-control"),
            form.Button('Login',submit='submit' , class_="btn btn-primary"),
            validators = [
                form.Validator('Incorrect email / password combination.',
                               lambda i: users.is_correct_password(i.email, i.password)),
            ]
        )

class Logout:
    def GET(self):
        session.logout()
        raise web.seeother('/')

class Profile:
    @session.login_required
    def GET(self):
        f = mww.MyForm(self.register_detail_form(),'/Profile')
        f.form.fill(utils.extract_info_from_storage_by_list(session.get_session(),PROPERTY_LIST))
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Profile',f.render_css())
        return render.l3r9(left=l.render(),right=r.render())

    @session.login_required
    def POST(self):
        ipt = web.input(_unicode=True)
        f = mww.MyForm(self.register_detail_form(),'/Profile')
        if not f.form.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Profile',f.render_css())
            return render.l3r9(left=l.render(),right=r.render())
        else:
            users.update(session.get_session().uid,
                         **utils.extract_info_from_storage_by_list(ipt,PROPERTY_LIST))
            session.login(session.get_session().email)
            return "success"

    def register_detail_form(self):
        return form.Form(
            form.Textbox('email',
                         description="email",
                         class_="form-control"),
            form.Button('Save Change', submit='submit' , class_="btn btn-primary")
        )

class ResetPassword:
    @session.login_required
    def GET(self):
        f = mww.MyForm(self.reset_password_form(),'/ResetPassword')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Reset Password',f.render_css())
        return render.l3r9(left=l.render(),right=r.render())

    @session.login_required
    def POST(self):
        ipt = web.input(_unicode=True)
        f = self.reset_password_form()
        if not f.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Reset Password',f.render_css())
            return render.l3r9(left=l.render(),right=r.render())
        else:
            users.reset_password(session.get_session().uid,ipt.new_password)
            return "success"

    def reset_password_form(self):
        return form.Form(
            form.Password('new_password',
                          form.notnull,
                          form.Validator('Your password must at least 5 characters long.',
                                         lambda x: users.is_valid_password(x)),
                          description='New Password',
                          class_="form-control"),
            form.Password('re_password',
                          form.notnull,
                          description='确认密码',
                          class_="form-control"),
            form.Button('Reset Password' , submit='submit' , class_="btn btn-primary"),
            validators= [
                form.Validator('Password Not Match!.',
                               lambda i:i.new_password == i.re_password)
            ]
        )

class ResendPassword:
    # TODO ResendPassword
    @session.login_required
    def GET(self):
        return 'Hello, resend !! this is not implement, should config your mail server first !!'
