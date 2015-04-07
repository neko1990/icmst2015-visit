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
u"矿业工程学院",u"安全工程学院",u"力学与建筑工程学院",u"机电工程学院",u"资源与地球科学学院",u"化工学院",u"环境与测绘学院",
u"电力工程学院",u"材料科学与工程学院",u"理学院",u"计算机科学与技术学院",u"管理学院",u"文学与法政学院",u"马克思主义学院",
u"外国语言文化学院",u"艺术与设计学院",u"体育学院",u"孙越崎学院",u"国际学院",u"应用技术学院",u"成人教育学院",u"其他",
]

class Application:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/cumt/ApplicationRoute')
        f = mww.MyForm(self.registration_form(),'/cumt/Application')
        user = users.get_user_by_uid(session.get_session().uid)
        f.form.fill(user)
        p = mww.Panel(u'提交申请',f.render_css())
        return render.l12( page = p.render())

    def POST(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/cumt/ApplicationRoute')
        ipt = web.input(_unicode=True)
        f = mww.MyForm(self.registration_form(),'/cumt/Application')
        if not f.form.validates(ipt):
            p = mww.Panel('Application',f.render_css())
            return render.l12( page = p.render())
        regid = users.add_reg(session.get_session().uid,f.form.d)
        p = mww.Panel(u'提交申请',u'申请已提交，点击<a href="/cumt/Application">这里</a>进行修改')
        return render.l12( page = p.render())

    def registration_form(self):
        return form.Form(
            form.Dropdown('college',
                          [u'==请选择您所在学院==']+CUMTSchoolList,
                          form.Validator("select college.",
                                         lambda i:i in CUMTSchoolList),
                          form.notnull,
                          description=u"* 学院",
                          class_="form-control"),
            form.Textbox('telephone',form.notnull,
                         description=u"* 手机号码",
                         class_="form-control"),
            mww.MyRadio('gender',
                        [u'男',u'女'],
                        form.notnull,
                        description=u"* 性别"),
            form.Textbox('studentid',form.notnull,description=u'* 学号',class_="form-control"),
            form.Textbox('name',form.notnull,description=u'* 姓名',class_="form-control"),
            form.Button('submit', submit='submit',class_="btn btn-primary",html=u"保存修改")
        )

class ApplicationRoute:
    def GET(self):
        if session.get_session().privilege == 1:
            raise web.seeother('/cumt/SendApplication')
        return render.application_route()

class SendApplication:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/cumt/ApplicationRoute')
        # if users.is_registered(session.get_session().uid):
        #     return render.application()
        return render.send_application()
