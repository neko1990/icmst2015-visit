import web
import config

import app.controllers
from app.helpers import session
from app.models import articles


urls = (
    '/',                               'app.controllers.index.Index',
    '/CallForPaper',                   'app.controllers.index.CallForPaper',
    '/Article',                        'app.controllers.index.Article',

    '/SignUp',                         'app.controllers.account.SignUp',
    '/Login',                          'app.controllers.account.Login',
    '/Logout',                         'app.controllers.account.Logout',
    '/Profile',                        'app.controllers.account.Profile',
    #'/ResendPassword',                 'app.controllers.account.ResendPassword',
    '/ResetPassword',                  'app.controllers.account.ResetPassword',

    '/Application',                    'app.controllers.attendant.Application',
    '/SendApplication',                'app.controllers.attendant.SendApplication',
    '/ApplicationRoute',               'app.controllers.attendant.ApplicationRoute',

    '/UserManage',                     'app.controllers.admin.UserManage',
    '/ResetUserPassword',              'app.controllers.admin.ResetUserPassword',

    '/AddArticle',                     'app.controllers.articlemanage.AddArticle',
    '/DelArticle',                     'app.controllers.articlemanage.DelArticle',
    '/AlterArticle',                   'app.controllers.articlemanage.AlterArticle',

    '/UserDetail',                     'app.controllers.detail.UserDetail',

    '/RegReport',                      'app.controllers.report.RegReport',

    '/(?:img|js|css)/.*',              'app.controllers.public.public',
    '/download',                       'app.controllers.public.received',
)

app = web.application(urls,globals())
session.add_sessions_to_app(app)
web.config._title_list = articles.gen_title_list()

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
