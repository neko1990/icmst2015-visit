# -*- coding: utf-8 -*-
from web import safeunicode

from app.models import users

from app.helpers import session
from app.helpers import mywebwidgets as mww

from config import render

class RegReport:
    @session.privilege_match(5)
    def GET(self):
        schema = [['uid',u"用户编号",'col-sm-1'],
                  ['email',u"邮箱",'col-sm-1'],
                  ['telephone',u'手机号码','col-sm-1'],
                  ['gender',u'性别','col-sm-1'],
                  ['studentid',u'学号','col-sm-1'],
                  ['college',u'学院','col-sm-1'],
                  ['name',u'姓名','col-sm-1']]
        rs = users.get_all_registrations()
        t = mww.Table(schema,
                      rs,
                      class_='table table-striped table-hover display')
        return render.report( table =t.render())
