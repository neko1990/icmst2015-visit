import web
from web import form
from web import  Storage
from web.utils import safeunicode
import time

from app.helpers import session
from app.helpers import mywebwidgets as mww
from app.helpers.utils import file_record_trans_to_display

from app.helpers.forms import registration_form
from app.helpers.forms import sendapply_form
from app.helpers.forms import login1_form
from app.helpers.forms import register1_form

from app.models import users
from app.models import reg

from config import render

class Registration:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/RegistrationGate')
        f = mww.MyForm(registration_form(),'/Registration')
        p = mww.Panel('Application',f.render_css())
        return render.l12(p.render())

    def POST(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/RegistrationGate')
        ipt = web.input(_unicode=True)
        f = mww.MyForm(registration_form(),'/Registration')
        if not f.form.validates(ipt):
            p = mww.Panel('Application',f.render_css())
            return render.l12(p.render())
        regid = reg.add_reg(f.form.d)
        reg.write_reg_log(session.get_session().uid,regid)
        p = mww.Panel('Application','Thank you form your Application!')
        return render.l12(p.render())

content_template = '''<div class="row"><div class="col-md-1"></div>
<div class="col-md-10">
<ul>
<li>Start your online registration.</li>
<li>Please refer to the Bank Transfer Information for payment as soon as possible.</li>
<li>We accept abstracts or presentation summaries, but we do welcome full paper contributions, please submit your full paper online now.</li>
<li>To obtain an invitation letter from the organizing committee for visa application, please advise us of your request via E-mail.</li>
<li>For new registrations, please create a new account below by entering your email address and password information. For existing registrations, use the login panel to the right.</li>
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

content_template1 = '''<div class="row"><div class="col-md-1"></div>
<div class="col-md-10">
<ul>
<li>Start your online registration.</li>
<li>Please refer to the Bank Transfer Information for payment as soon as possible.</li>
<li>We accept abstracts or presentation summaries, but we do welcome full paper contributions, please submit your full paper online now.</li>
<li>To obtain an invitation letter from the organizing committee for visa application, please advise us of your request via E-mail.</li>
<li>For new registrations, please create a new account below by entering your email address and password information. For existing registrations, use the login panel to the right.</li>
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
        ssif = mww.MyForm(login1_form(),'/Login',method="get")
        ssuf = mww.MyForm(register1_form(),'/Register',method="get")
        content = content_template % (ssuf.render_css(),ssif.render_css())
        p = mww.Panel('ICMST2015 Conference Visit Application',content)
        return render.l12(p.render())

class SendApply:
    def GET(self):
        if session.get_session().privilege != 1:
            raise web.seeother('/RegistrationGate')
        send = mww.MyForm(sendapply_form(),'/Registration',method="get")
        content = content_template1 % (send.render_css())
        p = mww.Panel('Apply',content)
        return render.l12(p.render())

