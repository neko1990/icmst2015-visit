# -*- coding: utf-8 -*-
import web
from web import form
from web import  Storage
from web.utils import safeunicode
import time

from app.helpers import session
from app.helpers import mywebwidgets as mww
from app.helpers.utils import file_record_trans_to_display

from app.models import users
from app.models import reg

from config import render

CUMTSchoolList = [
'mining','computer'
]

class Registration:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/RegistrationGate')
        f = mww.MyForm(self.registration_form(),'/Registration')
        p = mww.Panel('Application',f.render_css())
        return render.l12( page = p.render())

    def POST(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/RegistrationGate')
        ipt = web.input(_unicode=True)
        f = mww.MyForm(self.registration_form(),'/Registration')
        if not f.form.validates(ipt):
            p = mww.Panel('Application',f.render_css())
            return render.l12( page = p.render())
        regid = reg.add_reg(f.form.d)
        reg.write_reg_log(session.get_session().uid,regid)
        p = mww.Panel('Application','Thank you form your Application!')
        return render.l12( page = p.render())

    def registration_form(self):
        return form.Form(
            form.Dropdown('college',
                          ['-seclect college-']+CUMTSchoolList,
                          form.Validator("select college.",
                                         lambda i:i in CUMTSchoolList),
                          form.notnull,
                          description="* college",
                          class_="form-control"),
            form.Textbox('telephone',form.notnull,
                         description='* Telephone',
                         class_="form-control"),
            mww.MyRadio('gender',
                        ['Female','Male'],
                        value="Male",
                        description="* gender"),
            form.Textbox('num',form.notnull,description='* Student ID',class_="form-control"),
            form.Textbox('name',form.notnull,description='* Name',class_="form-control"),
            form.Button('submit', submit='submit',class_="btn btn-primary")
        )


content_template = u'''<div class="row"><div class="col-md-1"></div>
<div class="col-md-10">
<ul>
<li>第一点</li>
<li>第二点</li>
<li>第三点</li>
</ul>
</div>
<div class="col-md-1"></div>
</div>
<div class="row">
<h3>&nbsp;</h3>
</div>
<div class="row">
<div class="col-md-4"></div>
<div class="col-md-2">%s</div>
<div class="col-md-2">%s</div>
<div class="col-md-4"></div>
</div>'''

content_template1 = u'''<div class="row"><div class="col-md-1"></div>
<div class="col-md-10">
<ul>
<li>第一点</li>
<li>第二点</li>
<li>第三点</li>
</ul>
</div>
<div class="col-md-1"></div>
</div>
<div class="row">
<h3>&nbsp;</h3>
</div>
<div class="row">
<div class="col-md-4"></div>
<div class="col-md-4">%s</div>
<div class="col-md-4"></div>
</div>'''

class RegistrationGate:
    def GET(self):
        if session.get_session().privilege == 1:
            raise web.seeother('/SendApply')
        ssif = mww.MyForm(self.login1_form(),'/Login',method="get")
        ssuf = mww.MyForm(self.register1_form(),'/Register',method="get")
        content = content_template % (ssuf.render_css(),ssif.render_css())
        p = mww.Panel(u'ICMST2015 会议参观申请',content)
        return render.l12( page = p.render())

    def login1_form(self):
        return form.Form(
            form.Button('Login', submit='submit' , class_="btn btn-primary")
        )

    def register1_form(self):
        return form.Form(
            form.Button('Register', submit='submit' , class_="btn btn-primary")
        )

class SendApply:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/RegistrationGate')
        send = mww.MyForm(self.sendapply_form(),'/Registration',method="get")
        content = content_template1 % (send.render_css())
        p = mww.Panel('Apply',content)
        return render.l12( page = p.render())

    def sendapply_form(self):
        return form.Form(
            form.Button('submit', submit='submit',class_="btn btn-primary")
        )
