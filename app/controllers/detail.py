# -*- coding: utf-8 -*-
import web
from web import Storage

from app.helpers import session
from app.helpers import mywebwidgets as mww

from app.models import users

from config import render

class UserDetail:
    @session.privilege_match([1,2,5])
    def GET(self):
        ipt = web.input(_unicode=True)
        if 'uid' not in ipt:
            return "Argument Error"
        if users.uid_exist_p(ipt.uid):
            user = users.get_user_by_uid(ipt.uid)
        else:
            return "User Not Exist!"

        _s = session.get_session()
        _p = _s.privilege
        # if attendant, only allowed to check himself.
        if _p == 1:
            if _s.uid != user.uid:
                return "Action Not Allowed!"

        # check done. do the real work
        schema_user = [['uid',u"用户编号",'col-sm-1'],
                       ['email',u"邮箱",'col-sm-1'],
                       ['telephone',u'手机号码','col-sm-1'],
                       ['gender',u'性别','col-sm-1'],
                       ['studentid',u'学号','col-sm-1'],
                       ['college',u'学院','col-sm-1'],
                       ['name',u'姓名','col-sm-1']]

        t_user = mww.MyVerticalTable(schema_user,
                                     user,
                                     class_='table table-striped table-hover')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Detailed Information',t_user.render())
        return render.l3r9(left = l.render(),right = r.render())
