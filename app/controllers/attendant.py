# -*- coding: utf-8 -*-
import web
from web import form
from web import  Storage
from web.utils import safeunicode
import time

from app.helpers import session
from app.helpers import mywebwidgets as mww

from app.models import users

from config import render

CUMTSchoolList = [
'mining','computer'
]

class Application:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/ApplicationRoute')
        f = mww.MyForm(self.registration_form(),'/Application')
        user = users.get_user_by_uid(session.get_session().uid)
        f.form.fill(user)
        p = mww.Panel('Application',f.render_css())
        return render.l12( page = p.render())

    def POST(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/ApplicationRoute')
        ipt = web.input(_unicode=True)
        f = mww.MyForm(self.registration_form(),'/Application')
        if not f.form.validates(ipt):
            p = mww.Panel('Application',f.render_css())
            return render.l12( page = p.render())
        regid = users.add_reg(session.get_session().uid,f.form.d)
        p = mww.Panel('Application','Thank you form your Application!')
        return render.l12( page = p.render())

    def registration_form(self):
        return form.Form(
            form.Dropdown('college',
                          ['-seclect college-']+CUMTSchoolList,
                          form.Validator("select college.",
                                         lambda i:i in CUMTSchoolList),
                          form.notnull,
                          description=u"* 学院",
                          class_="form-control"),
            form.Textbox('telephone',form.notnull,
                         description=u"* 手机号码",
                         class_="form-control"),
            mww.MyRadio('gender',
                        ['Male','Female'],
                        value="Male",
                        description=u"* 性别"),
            form.Textbox('studentid',form.notnull,description=u'* 学号',class_="form-control"),
            form.Textbox('name',form.notnull,description=u'* 姓名',class_="form-control"),
            form.Button('submit', submit='submit',class_="btn btn-primary")
        )


class ApplicationRoute:
    def GET(self):
        if session.get_session().privilege == 1:
            raise web.seeother('/SendApplication')
        return render.registration_gate()

class SendApplication:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/ApplicationRoute')
        return render.registration_gate1()
