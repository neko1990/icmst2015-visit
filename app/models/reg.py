import web
from web import Storage
from config import db

def add_reg(s):
    return db.insert('registration',
                     num=s.num,
                     college=s.college,
                     name=s.name,
                     telephone=s.telephone,
                     gender=s.gender
    )

def write_reg_log(uid,regid):
    db.insert('reg_journal',by_uid=uid,regid=regid)

def get_all_registrations():
    #return db.select('registration').list()
    return db.query('''select registration.*,reg_journal.by_uid as uid from registration LEFT JOIN reg_journal ON reg_journal.regid=registration.regid''').list()

