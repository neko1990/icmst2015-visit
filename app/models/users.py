import web
import hashlib

from config import db
from config import PASSWORD_SALT

def hash_password(passwd):
    return hashlib.sha1(PASSWORD_SALT+passwd).hexdigest()

def create_account(email, password, privilege ):
    email = email.lower()
    hashed_password = hash_password(password)
    db.insert('users',
              email=email,
              password=hashed_password,
              privilege=privilege)

def get_user_by_email(email):
    email = email.lower()
    return db.select('users',vars=dict(email=email),
                     where='email = $email')[0]

def email_exist_p(email):
    email = email.lower()
    return db.select(
        'users',
        vars = dict(email=email),
        what = 'count(uid) as c',
        where = 'email = $email')[0].c

def uid_exist_p(uid):
    return db.select(
        'users',
        vars = dict(uid=uid),
        what = 'count(uid) as c',
        where = 'uid = $uid')[0].c

def is_email_available(email):
    email = email.lower()
    return not email_exist_p(email)

def is_valid_password(password):
    return len(password) >= 5

def is_correct_password(email, password):
    email = email.lower()
    if is_email_available(email):
        return False
    user = get_user_by_email(email)
    in_db_pwd = user.get('password', False)
    return in_db_pwd == hash_password(password)

def update(uid, **kw):
    db.update('users', vars=dict(uid=uid), where='uid = $uid', **kw)

def reset_password(uid,new_password):
    db.update('users', vars=dict(uid=uid), where='uid = $uid',
              password=hash_password(new_password))

def get_users_by_privilege(p):
    return db.select('users',vars=dict(privilege=p),
                     where='privilege = $privilege').list()

def get_user_by_uid(uid):
    return db.select('users', vars=dict(uid=uid),where='uid = $uid')[0]

def get_all_users():
    return db.select('users')

def get_users_by_country(c):
    return db.select('users',vars=dict(country=c),where="country = $country").list();

def get_users_by_country_not(c):
    return db.select('users',vars=dict(country=c),where="country != $country").list();

def get_users_by_name(name):
    return db.select('users',vars = dict(name=name),where="name LIKE %$name%").list()

def user_grouped_fid_per_session():
    sql='''
SELECT uid, group_concat(fid) as submited_fid,group_concat(distinct(session)) as belong_session
  FROM (select fid,uid,session from files where status='accepted')
  GROUP BY uid,session
;'''
    return db.query(sql)


def add_reg(uid,s):
    with db.transaction():
        db.insert('reg_log',uid = uid ,
                  studentid=s.studentid,
                  college=s.college,
                  name=s.name,
                  telephone=s.telephone,
                  gender=s.gender,
        )
        db.update('users', vars = dict(uid=uid),
                  where = 'uid = $uid',
                  studentid=s.studentid,
                  college=s.college,
                  name=s.name,
                  telephone=s.telephone,
                  gender=s.gender,
        )
        return True
    return False

def get_all_registrations():
    return db.select('users',where='privilege==1 AND studentid NOT NULL' ).list()
    # return db.query('''select registration.*,reg_journal.by_uid as uid from registration LEFT JOIN reg_journal ON reg_journal.regid=registration.regid''').list()

def is_registered(uid):
    return db.select('users',vars=dict(uid=uid),where='uid=$uid AND studentid NOT NULL')
