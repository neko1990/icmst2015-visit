import web
from web import Storage
from config import db

def get_article_by_name(name):
    return db.select('articles',vars=dict(name=name),where = "name=$name").list()[0]

def name_exist_p(name):
    return db.select(
        'articles',
        vars = dict(name=name),
        what = 'count(aid) as c',
        where = 'name = $name')[0].c

def add_article(name,title,content,parent="NOPARENT",has_child_p=0):
    db.insert('articles',name=name,title=title,content=content,parent=parent,has_child_p=has_child_p)

def get_articles_by_parent(parent_name):
    return db.select('articles',vars=dict(name=parent_name),where='parent = $name').list()

def update(aid,**kw):
    db.update('articles', vars=dict(aid=aid), where='aid = $aid', **kw)

def parent_sans_p(parent):
    return parent == "NOPARENT" or name_exist_p(parent)

def del_article_by_name(name):
    db.delete('articles',vars=dict(name=name),where="name=$name")

def get_article_by_aid(aid):
    return db.select('articles',vars=dict(aid=aid),where='aid = $aid').list()[0]

def get_all_first_level():
    return map(lambda x:x.name,get_articles_by_parent("NOPARENT"))

def gen_title_list():
    def add_child(e):
        if e.has_child_p:
            lines = e.content.split('\n')
            child =  []
            for line in lines:
                line = line.strip()
                if len(line)==0:
                    break
                name,title = line.split(':')
                if name.startswith("#"):
                    continue
                child.append(Storage(name=name,title=title))
            e.child = child
        else:
            e.child = []
        return e
    return [add_child(e) for e in get_index()]

def get_index():
    idx = get_article_by_name("INDEX")
    lines = idx.content.split('\n')
    nav = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            break
        name,title=line.split(':')
        if  not name_exist_p(name):
            continue
        nav.append(get_article_by_name(name))
    return nav


def get_all_articles():
    return db.select('articles').list()
