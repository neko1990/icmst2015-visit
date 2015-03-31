from web import safeunicode

from app.models import reg

from app.helpers import session
from app.helpers import mywebwidgets as mww
from app.helpers.utils import file_record_trans_to_display

from config import render

def report_render(content):
    template = '''
<html>
<head>
<meta charset="utf-8">
<!-- DataTables CSS -->
<link rel="stylesheet" type="text/css" href="/static/css/jquery.dataTables.css">
<script type="text/javascript" charset="utf8" src="/static/js/jquery.js"></script>
<!-- DataTables -->
<script type="text/javascript" charset="utf8" src="/static/js/jquery.dataTables.js"></script>
</head>
<body>
%s
<script>
$(document).ready( function (){
$('.table_class').DataTable({"paging":false,"scrollX":true});
});
</script>
</body>
</html>
    '''
    return template % content


class RegReport:
    @session.privilege_match(5)
    def GET(self):
        schema = [['regid','regid'],
                  ['uid','uid'],
                  ['name','name'],
                  ['telephone','telephone'],
                  ['college','college'],
                  ['num','num']
                  ]
                  
        rs = reg.get_all_registrations()
        t = mww.Table(schema,
                      rs,
                      class_='table table-striped table-hover display')
        return report_render(t.render())


