import web
from web import form

from app.helpers import mywebwidgets as mww

from app.models import users
from app.models import articles

from config import COUNTRY_LIST

### account.py ###

vemail = form.regexp(r'.+@.+', 'Please enter a valid email address')

login_form = form.Form(
    form.Textbox('email',
                 form.notnull, vemail,
                 description='Email',
                 class_="form-control"),
    form.Password('password',
                  form.notnull,
                  description='Password',
                  class_="form-control"),
    form.Button('Login', submit='submit' , class_="btn btn-primary"),
    validators = [
        form.Validator('Incorrect email / password combination.',
                       lambda i: users.is_correct_password(i.email, i.password)),
    ]
)

login1_form=form.Form(
    form.Button('Login', submit='submit' , class_="btn btn-primary")
)

register_detail_form = form.Form(
    form.Textbox('email',
                 description="email",
                 class_="form-control"),
    form.Button('Save Change', submit='submit' , class_="btn btn-primary")
)

reset_password_form = form.Form(
    form.Password('new_password',
                  form.notnull,
                  form.Validator('Your password must at least 5 characters long.',
                                 lambda x: users.is_valid_password(x)),
                  description='New Password',
                  class_="form-control"),
    form.Password('re_password',
                  form.notnull,
                  description='Confirm Password',
                  class_="form-control"),
    form.Button('Reset Password' , submit='submit' , class_="btn btn-primary"),
    validators= [
        form.Validator('Password Not Match!.',
                       lambda i:i.new_password == i.re_password)
    ]
)

register_form = form.Form(
    form.Textbox('email',
                 form.notnull, vemail,
                 form.Validator('This email address is already taken.',
                                lambda x: users.is_email_available(x)),
                 description='* Email ',
                 class_="form-control"),
    form.Password('password',
                  form.notnull,
                  form.Validator('Password must at least 5 characters long.',
                                 lambda x: users.is_valid_password(x)),
                  description='* Password',
                  class_="form-control"),
    form.Password('re_password',
                  form.notnull,
                  description="* Confirm Password",
                  class_="form-control"),
    form.Button('Sign Up', type='submit', value='Register' , class_="btn btn-primary"),
    validators = [
        form.Validator('Password Not Match!.', lambda i:i.password == i.re_password)
    ]
)

register1_form = form.Form(
    form.Button('Register', submit='submit' , class_="btn btn-primary")
)

forgot_password_form = form.Form(
    form.Textbox('email',
        form.notnull, vemail,
        form.Validator('There is no record of this email in our database.',
        lambda x: not users.is_email_available(x)),
        description='Email'),
    form.Button('submit', type='submit', value='Register' , class_="btn btn-primary"),
)


### admin.py ###

send_mail_form = form.Form(
    form.Textbox('send_to:',form.notnull,class_="form-control"),
    form.Textbox('subject:',form.notnull,class_="form-control"),
    form.Textarea('body:',form.notnull,class_="form-control"),
    form.Button('submit',submit='submit',class_="btn btn-primary")
)

user_search_form = form.Form(
    form.Textbox('uid',class_="form-control"),
    form.Textbox('name',class_="form-control"),
    form.Textbox('email',class_="form-control"),
    form.Dropdown('country',['All','China','Other'],class_="form-control"),
    form.Button('query',type='sbumit',class_="btn btn-primary")
)

reset_user_password_form = form.Form(
    form.Textbox('uid',
                 form.notnull,
                 description='Uid',
                 class_="form-control"),
    form.Password('new_password',
                  form.notnull,
                  form.Validator('Your password must at least 5 characters long.',
                                 lambda x: users.is_valid_password(x)),
                  description='New Password',
                  class_="form-control"),
    form.Password('re_password',
                  form.notnull,
                  description='Confirm Password',
                  class_="form-control"),
    form.Button('Reset Password' , submit='submit' , class_="btn btn-primary"),
    validators= [
        form.Validator('Password Not Match!.',
                       lambda i:i.new_password == i.re_password)
    ]
)


## for registration
registration_form = form.Form(
    
    form.Dropdown('college',
                  ['-seclect college-']+COUNTRY_LIST,
                  form.Validator("select college.",
                                 lambda i:i in COUNTRY_LIST),
                  form.notnull,
                  description="* college",
                  class_="form-control"),
    form.Textbox('telephone',form.notnull,
                 description='* Telephone',
                 class_="form-control"),
    mww.MyRadio('gender',
                ['Female','Male'],
                value="Male",
                description="* gender"),
    form.Textbox('num',form.notnull,description='* Student ID',class_="form-control"),
    form.Textbox('name',form.notnull,description='* Name',class_="form-control"),
    form.Button('submit', submit='submit',class_="btn btn-primary")
)

sendapply_form = form.Form(
    form.Button('submit', submit='submit',class_="btn btn-primary")
)
simple_sign_up_form = form.Form(
    form.Textbox('email',
                 form.notnull, vemail,
                 form.Validator('This email address is already taken.',
                                lambda x: users.is_email_available(x)),
                 description='Email ',
                 class_="form-control"),
    form.Password('password',
                  form.notnull,
                  form.Validator('Password must at least 5 characters long.',
                                 lambda x: users.is_valid_password(x)),
                  description='Password',
                  class_="form-control"),
    form.Password('re_password',
                  form.notnull,
                  description="Confirm Password",
                  class_="form-control"),
    form.Button('Sign Up', type='submit', value='Register' , class_="btn btn-primary"),
    validators = [
        form.Validator('Password Not Match!.', lambda i:i.password == i.re_password)
    ]
)
