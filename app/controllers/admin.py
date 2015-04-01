# -*- coding: utf-8 -*-
import web
from web import form
from web import Storage

from app.helpers import session
from app.helpers import mywebwidgets as mww

from app.models import users

from config import render

def user_record_trans_to_display(r):
    return Storage(operations='<a href="%s">%s</a>' % ('/UserDetail?uid=%d' % (r.get('uid')),'Detail'),
                   **r)


class UserManage:
    @session.privilege_match(5)
    def GET(self):
        myf = mww.MyForm(self.user_search_form(),'/UserManage')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('User Management',myf.render_css())
        return render.l3r9(left=l.render(),right=r.render())

    @session.privilege_match(5)
    def POST(self):
        ipt = web.input(_unicode=True)
        #print ipt
        f = self.user_search_form()
        myf = mww.MyForm(f,'/UserManage')
        if not f.validates(ipt):
            return "Argument Error"
        if len(ipt.uid)>0:
            if users.uid_exist_p(ipt.uid):
                us = [users.get_user_by_uid(ipt.uid)]
            else:
                us = []
        elif len(ipt.name)>0:
            us = users.get_users_by_name(ipt.name)
        elif len(ipt.email)>0:
            if users.email_exist_p(ipt.email):
                us = [users.get_user_by_email(ipt.email)]
            else:
                us = []
        elif ipt.country == 'All':
            us = users.get_all_users()
        elif ipt.country == 'China':
            us = users.get_users_by_country('China')
        elif ipt.country == 'Other':
            us = users.get_users_by_country_not('China')
        else:
            us = []
        schema = [['uid',"Index"],
                  ['name',"Name"],
                  ['country',"Country"],
                  ['email',"Email"],
                  ['operations',"Operations"]]
        t = mww.Table(schema,
                      map(user_record_trans_to_display,us),
                      class_='table table-striped table-hover')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('User Management',myf.render_css()+t.render())
        return render.l3r9(left=l.render(),right=r.render())

    def user_search_form(self):
        return form.Form(
            form.Textbox('uid',class_="form-control"),
            form.Textbox('name',class_="form-control"),
            form.Textbox('email',class_="form-control"),
            form.Dropdown('country',['All','China','Other'],class_="form-control"),
            form.Button('query',type='sbumit',class_="btn btn-primary")
        )

class ResetUserPassword:
    @session.privilege_match(5)
    def GET(self):
        f = mww.MyForm(self.reset_user_password_form(),'/ResetUserPassword')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Reset User Password',f.render_css())
        return render.l3r9(left=l.render(),right=r.render())

    @session.privilege_match(5)
    def POST(self):
        ipt = web.input(_unicode=True)
        f = self.reset_user_password_form()
        if not f.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Reset User Password',f.render_css())
            return render.l3r9(left=l.render(),right=r.render())
        else:
            users.reset_password(ipt.uid,ipt.new_password)
            return "success"
    def reset_user_password_form(self):
        return form.Form(
            form.Textbox('uid',
                         form.notnull,
                         description='Uid',
                         class_="form-control"),
            form.Password('new_password',
                          form.notnull,
                          form.Validator('Your password must at least 5 characters long.',
                                         lambda x: users.is_valid_password(x)),
                          description='New Password',
                          class_="form-control"),
            form.Password('re_password',
                          form.notnull,
                          description='Confirm Password',
                          class_="form-control"),
            form.Button('Reset Password' , submit='submit' , class_="btn btn-primary"),
            validators= [
                form.Validator('Password Not Match!.',
                               lambda i:i.new_password == i.re_password)
            ]
        )
