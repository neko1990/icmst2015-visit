import web
from web import Storage
from web import net
import os

from app.models import users

def extract_info_from_storage_by_list(s,l):
    d = {}
    for p in l:
        if p in s and s.get(p) is not None:
            d[p]=s.get(p)
    return d

def make_findex(i):
    assert i < 10000 , "file overflow"
    if i < 10:
        return 'ICM000'+ str(i)
    elif i < 100:
        return 'ICM00' + str(i)
    elif i < 1000:
        return 'ICM0' + str(i)
    elif i < 10000:
        return 'ICM' + str(i)

def file_record_trans_to_display(r,acts=[]):
    _findex = make_findex(r.fid)
    findex = '''<a href="/FileDetail?fid=%s">%s</a>''' % (r.fid,_findex)
    class_ = ""
    id_ = r.fid
    brief_p = r.get('brief_p')
    actions = ''
    for act in acts:
        if act in ['accept','reject','transfer']:
            actions += '<a class="btn btn-primary btn-xs btnact" \
            data-toggle="modal fade" data-target=".modal" \
            data-fid="%s" data-findex="%s" data-act="%s" \
            data-papertitle="%s">%s</a>' \
            % (r.fid,_findex,act,r.paper_title,act)
        elif act == 'download':
            actions += '''<a class="btn btn-primary btn-xs" \
            href="/download?name=%s" download="%s">Download</a>''' \
            % (r.savename,r.paper_title+'.'+r.ext)
        elif act == 'cancel':
            actions +=  '<a class="hidden btn btn-primary btn-xs btnact"\
            data-toggle="modal fade" data-target=".modal" \
            data-fid="%s" data-findex="%s" data-act="%s" \
            data-papertitle="%s">%s</a>' \
            % (r.fid,_findex,act,r.paper_title,act)
        elif act == 'modify':
            actions +=  '<a class="btn btn-primary btn-xs btnact"\
            data-toggle="modal fade" data-target=".modal" \
            data-fid="%s" data-findex="%s" data-act="%s" \
            data-papertitle="%s">%s</a>' \
            % (r.fid,_findex,act,r.paper_title,act)
    if len(actions)>0:
        actions = '''<div class="btn-group">%s</div>''' %(actions)
    if r.status == "new":
        class_ = "success"
    if r.status == "rejected":
        class_ = "danger"
    if brief_p == 1:
        _type = "Brief"
    elif brief_p == 0:
        _type = "Extended"
    else:
        _type = ""
    return Storage(findex = findex,
                   class_ = class_,
                   id_ = id_,
                   _type = _type,
                   actions = actions,
                   **r)

def journal_record_trans_to_display(r):
    _findex= make_findex(r.fid)
    findex = '''<a href="/FileDetail?fid=%s">%s</a>''' % (r.fid,_findex)
    u = users.get_user_by_uid(r.by_uid)
    if u.privilege == 5:
        by = 'admin'
    elif u.privilege == 2:
        by = 'officer'
    else:
        by = 'user'
    return Storage(
        findex = findex,
        by = by,
        **r
    )
