# -*- coding: utf-8 -*-
import web
from web import form
from web import Storage

from app.helpers import session
from app.helpers import mywebwidgets as mww

from app.helpers.forms import reset_user_password_form
from app.helpers.forms import user_search_form

from app.models import users

from config import render


def user_record_trans_to_display(r):
    return Storage(operations='<a href="%s">%s</a>' % ('/UserDetail?uid=%d' % (r.get('uid')),'Detail'),
                   **r)


class UserManage:
    @session.privilege_match(5)
    def GET(self):
        myf = mww.MyForm(user_search_form(),'/UserManage')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('User Management',myf.render_css())
        return render.l3r9(l.render(),r.render())

    @session.privilege_match(5)
    def POST(self):
        ipt = web.input(_unicode=True)
        #print ipt
        f = user_search_form()
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
        return render.l3r9(l.render(),r.render())


class ResetUserPassword:
    @session.privilege_match(5)
    def GET(self):
        f = mww.MyForm(reset_user_password_form(),'/ResetUserPassword')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Reset User Password',f.render_css())
        return render.l3r9(l.render(),r.render())

    @session.privilege_match(5)
    def POST(self):
        ipt = web.input(_unicode=True)
        f = reset_user_password_form()
        if not f.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Reset User Password',f.render_css())
            return render.l3r9(l.render(),r.render())
        else:
            users.reset_password(ipt.uid,ipt.new_password)
            return "success"
