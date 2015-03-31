from web import net
from web import form


class Table:
    def __init__(self, schema , lstorage , class_ ='table'):
        self.schema = schema
        self.lstorage =  lstorage
        self.class_ = class_

    def render(self):
        if len(self.class_)>0:
            out = '<div class="bs-component"><table class="table_class %s" cellspacing="0" width="100%%">\n' % (self.class_)
        else:
            out = '<table id="table_id">\n'
        out += self.render_schema()

        out += '<tbody>\n'
        for s in self.lstorage:
            out+='<tr'
            if ('class_' in s) and len(s.class_) > 0:
                out += ' class="%s"' % (s.class_)
            if 'id_' in s:
                out += ' id="trline-%s"' % (s.id_)
            out += '>\n'
            for i in self.schema:
                out += '<td>%s</td>\n' % (s.get(i[0]))
            out += '</tr>\n'
        out += '</tbody>\n'
        out += '</table></div>\n'
        return out

    render_css = render

    def render_schema(self):
        out = '<thead>\n<tr>\n'
        if len(self.schema[0]) == 2:
            for i in self.schema:
                out += '<th class="">%s</th>\n' % (net.websafe(i[1]))
        elif len(self.schema[0]) ==3:
            for i in self.schema:
                out += '<th class="%s">%s</th>\n' % (i[2],net.websafe(i[1]))
        out += '</tr>\n</thead>\n'
        return out

class MyVerticalTable:
    def __init__(self,schema,record,class_='table'):
        self.record = record
        self.schema = schema
        self.class_ = class_
    def render(self):
        out=['<div class="bs-componet"><table class="%s">' % (self.class_)]
        out.append('<tbody>')
        for s in self.schema:
            l = '<tr><td>%s</td> <td>%s</td></tr>' % (s[1],self.record[s[0]])
            out.append(l)
        out.append('</tbody></table></div>')
        return ''.join(out)

    render_css = render

class MyForm:
    """add div wrapper for webpy form, useful for custom css class."""
    def __init__(self, form, callback, divcss=None, formcss="form-horizontal",method="post"):
        self.form = form
        self.formcss = formcss
        self.divcss = divcss
        self.callback = callback
        self.method = method

    def render(self):
        if self.divcss:
            out = '<div class="%s">' % self.divcss
        else:
            out = ''
        out += '<form method="%s" class="%s" action="%s">' % (self.method,self.formcss, self.callback)
        out += self.form.render()
        out += '</form>'
        if self.divcss:
            out += '</div>'
        return out
    def myrendernote(self,iid,note):
        if note: return """<label class="control-label" for="%s">%s</label>""" % (iid,note)
        return ""
    def myformrendernote(self,note):
        if note: return """<p class="text-warning">%s</p>""" % (note)
        return ""
    def render_css(self):
        """
        modified original form render_css. add div for every input
        """
        out = ['<form method="%s" class="%s" action="%s" enctype="multipart/form-data">\n' %
               (self.method,self.formcss, self.callback), self.myformrendernote(self.form.note)]
        # for upload reason, add enctype
        for i in self.form.inputs:
            if not i.is_hidden():
                iclass = "form-group"
                if i.note:
                    iclass += " has-error"
                out.append('<div class="%s">\n<label class="col-sm-3 control-label" for="%s">%s</label>\n' %
                           (iclass,i.id, net.websafe(i.description)))
            out.append(i.pre)
            out.append('<div class="col-sm-9">\n')
            out.append(i.render())
            out.append(self.myrendernote(i.id,i.note))
            out.append(i.post)
            if not i.is_hidden():
                out.append('</div>\n</div>\n')
            else:
                out.append('</div>\n')
        out.append('</form>')
        return ''.join(out)


class MyRadio(form.Input):
    def get_type(self):
        pass

    def __init__(self, name, args, *validators, **attrs):
        self.args = args
        super(MyRadio, self).__init__(name, *validators, **attrs)

    def render(self):
        out = ''
        for arg in self.args:
            out += '<div class="radio"><label>'
            if isinstance(arg, (tuple, list)):
                value, desc = arg
            else:
                value, desc = arg, arg
            attrs = self.attrs.copy()
            attrs['name'] = self.name
            attrs['type'] = 'radio'
            attrs['value'] = value
            if self.value == value:
                attrs['checked'] = 'checked'
            out += '<input %s> %s' % (attrs, net.websafe(desc))
            out += '</label></div>'
        return out

class Panel:
    def __init__(self, head=None, body=None, afterbody=None, foot=None):
        self.head = head
        self.body = body
        self.afterbody = afterbody
        self.foot = foot

    def render(self):
        res = '''<div class="panel panel-default">\n'''
        if self.head is not None:
            res += '''<div class="panel-heading"><h3 class="panel-title">%s</h3></div>\n''' \
                   % self.head
        if self.body is not None:
            res += '''<div class="panel-body">%s</div>\n''' % self.body
        if self.afterbody is not None:
            res += self.afterbody
        if self.foot is not None:
            res += '''<div class="panel-footer">%s</div>\n''' % self.foot
        res += '</div>'
        return res
    render_css = render


class ListGroup:
    """ item must be [[href link],[title]] """
    def __init__(self, items):
        self.items = items

    def render(self):
        res = '<ul class="list-group">\n'
        for item in self.items:
            res += '<li class="list-group-item"><a href=%s>%s</a></li>' % \
                   (item[0],item[1])
        res += '</ul>'
        return res
    render_css = render

modal = '''
<div class="modal fade" id="confirmModal" role="dialog" aria-labelledby="confirmModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">
        <span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
        </button>
        <h4 class="modal-title"></h4>
      </div>
      <div class="modal-body"></div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" id="actbtn"></button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
        '''
