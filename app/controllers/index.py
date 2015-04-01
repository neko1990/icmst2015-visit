import web

from app.models import articles
from config import render
from app.helpers import mywebwidgets as mww

class Index:
    def GET(self):
        raise web.seeother("/Article?name=Home")

class Article:
    def GET(self):
        ipt = web.input()
        if not 'name' in ipt:
            return "GET Request Format error"
        if not articles.name_exist_p(ipt.name):
            return "%s Page not exist" % ipt.name
        a = articles.get_article_by_name(ipt.name)
        if a.content.startswith('URL:'):
            raise web.seeother(a.content[4:])
        elif a.parent == "NOPARENT":
            return render.l12(page = a.content)
        else:
            parent = articles.get_article_by_name(a.parent)
            #TODO: use hash table, instead of liner look up table
            for p in web.config._title_list:
                if p.name == a.parent:
                    break
            left_links = map(lambda x:["Article?name="+x.name,x.title],
                             p.child)
            s = mww.ListGroup(left_links).render()
            l = mww.Panel(parent.title,None,s)
            r = mww.Panel(a.title,a.content)
            return render.l3r9(left=l.render(),right=r.render())
