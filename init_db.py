#-*- coding: utf-8 -*-
import sqlite3
import os
from web import utils

DB_NAME = 'db.sqlite3'

def create_tables():
    with open('sql.sql','r') as f:
        schema = f.read().strip()
    sdb = sqlite3.connect(DB_NAME)
    c= sdb.cursor()
    for s in schema.split(');'):
        if len(s) <= 1 :
            continue
        line = s+');'
        c.execute(line)
    sdb.commit()
    sdb.close()

def add_defaut_users():
    from app.models import users
    dft_pwd = '123456'
    users.create_account('neko1990@gmail.com','123456',5)
    users.create_account('1558063060@qq.com','123456',5)

    users.create_account('user1@gmail.com','123456',1)
    users.create_account('user2@gmail.com','123456',1)

def add_defaut_articles():
    from app.models import articles
    articles.add_article("INDEX","INDEX","Home:HomeHomeSweetHome\nICMST2015:ICMST2015","NOPARENT",1)
    articles.add_article("Home",u"申请观摩","URL:/cumt/ApplicationRoute","INDEX",0)
    articles.add_article("ICMST2015","ICMST2015","URL:http://icmst2015.cumt.edu.cn","INDEX",0)


if __name__ == '__main__':
    if DB_NAME in os.listdir('.'):
        os.remove(DB_NAME)
    create_tables()
    add_defaut_users()
    add_defaut_articles()
