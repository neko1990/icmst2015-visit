import web
from web import form

from app.models import articles

from app.helpers import session
from app.helpers import mywebwidgets as mww

from config import render

class AddArticle:
    @session.privilege_match(5)
    def GET(self):
        myf = mww.MyForm(self.add_article_form(),'/cumt/AddArticle')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Add New Article',myf.render_css())
        return render.l3r9(left=l.render(),right=r.render())

    def add_article_form(self):
        return form.Form(
            form.Textbox('name',
                         form.notnull,
                         form.Validator('name already exists.',
                                        lambda x: not articles.name_exist_p(x)),
                         description = 'Name:',
                         class_="form-control"),
            form.Textbox('title',form.notnull,description = 'Title:',class_="form-control"),
            #form.Textbox('parent',description="Parent Name"),
            form.Dropdown('parent',
                          ["NEW_TOPIC"]+articles.get_all_first_level(),
                          form.notnull,
                          description="Parent Name:",
                          class_="form-control"),
            form.Textarea('content',description="Content",class_="form-control",rows="10"),
            form.Button('submit', type='submit', value='OK Publish this article!!',class_="btn btn-primary"),
            validators = [
                form.Validator("Parent Not Exist. If this is a first level article, use 'NEW_TOPIC",
                               lambda i:(i.parent=="NEW_TOPIC" or articles.parent_sans_p(i.parent)))
            ]
        )

    @session.privilege_match(5)
    def POST(self):
        ipt = web.input(_unicode=True)
        f = self.add_article_form()
        myf = mww.MyForm(f,'/cumt/AddArticle')
        if not f.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Add New Article',myf.render_css())
            return render.l3r9(left=l.render(),right=r.render())
        else:
            if f.d.parent == "NEW_TOPIC":
                articles.add_article(f.d.name, f.d.title, f.d.content, "NOPARENT" )
            else:
                articles.add_article(f.d.name, f.d.title, f.d.content, f.d.parent )
            web.config._title_list = articles.gen_title_list()
            return "success"

class DelArticle:
    @session.privilege_match(5)
    def GET(self):
        myf = mww.MyForm(self.del_article_form(),'/cumt/DelArticle')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Del A Article',myf.render_css())
        return render.l3r9(left=l.render(),right=r.render())

    @session.privilege_match(5)
    def POST(self):
        ipt = web.input(_unicode=True)
        f = self.del_article_form()
        myf = mww.MyForm(f,'/cumt/DelArticle')
        if not f.validates(ipt):
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Del A Article',myf.render_css())
            return render.l3r9(left=l.render(),right=r.render())
        else:
            a = articles.get_article_by_name(ipt.name)
            leaves = articles.get_articles_by_parent(a.parent)
            assert len(leaves) > 1
            #parent = articles.get_article_by_name(a.parent)
            articles.del_article_by_name(ipt.name)
            web.config._title_list = articles.gen_title_list()
            return 'success'

    def del_article_form(self):
        return form.Form(
            form.Dropdown('name',
                          sorted(map(lambda x:x.name,articles.get_all_articles())),
                          form.notnull,
                          form.Validator('This Article Not Exist!',
                                         lambda x:articles.name_exist_p(x)),
                          description = "Delte Article Name:",
                          class_="form-control"),
            form.Button('submit', submit='submit', value='Delete it!',class_="btn btn-primary")
        )



class AlterArticle:
    @session.privilege_match(5)
    def GET(self):
        myf = mww.MyForm(self.article_select_form(),'/cumt/AlterArticle')
        s = mww.ListGroup(session.get_session().actions).render()
        l = mww.Panel('Settings',s)
        r = mww.Panel('Article Select',myf.render_css())
        return render.l3r9(left=l.render(),right=r.render())

    def article_select_form(self):
        return form.Form(
            form.Dropdown('article',
                          sorted(map(lambda x:x.name,articles.get_all_articles())),
                          form.notnull,
                          form.Validator('This Article Not Exist!',
                                         lambda x:articles.name_exist_p(x)),
                          description = "Article ",
                          class_="form-control"),
            form.Button('submit',type='submit',class_="btn btn-primary")
        )



    @session.privilege_match(5)
    def POST(self):
        ipt  = web.input(_unicode=True)
        if 'article' in ipt and articles.name_exist_p(ipt.article):
            article_info = articles.get_article_by_name(ipt.article)
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            aaf = mww.MyForm(self.alter_article_form()(article_info),'/cumt/AlterArticle')
            asf = mww.MyForm(self.article_select_form(),'/cumt/AlterArticle')
            asf.form.fill(ipt)
            r1 = mww.Panel('Article Select',asf.render_css())
            r2 = mww.Panel('Alter Article',aaf.render_css())
            return render.l3r9(left=l.render(),right=r1.render()+r2.render())

        elif 'name' in ipt and 'parent' in ipt and 'has_child_p' in ipt and articles.parent_sans_p(ipt.parent):
            # TODO result check
            articles.update(ipt.aid,content = ipt.content,title=ipt.title,parent=ipt.parent,has_child_p=ipt.has_child_p)
            web.config._title_list = articles.gen_title_list()
            return "success"
        else:
            myf = mww.MyForm(self.article_select_form(),'/cumt/AlterArticle')
            s = mww.ListGroup(session.get_session().actions).render()
            l = mww.Panel('Settings',s)
            r = mww.Panel('Article Select',myf.render_css())
            return render.l3r9(left=l.render(),right=r.render())

    def alter_article_form(self):
        return form.Form(
            form.Textbox('name',form.notnull,description='Name:',class_="form-control"),
            form.Textbox('title',form.notnull,description='Title:',class_="form-control"),
            form.Textbox('parent',form.notnull,description='parent:',class_="form-control"),
            form.Textbox('has_child_p',form.notnull,description='has_child_p:',class_="form-control"),
            form.Textarea('content',description="Content:",class_="form-control",rows="10"),
            form.Button('submit',type='submit',class_="btn btn-primary"),
            form.Hidden('aid')
        )
