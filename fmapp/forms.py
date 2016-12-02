from flask_wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators


class LoginForm(Form):
    username = TextField('user_name', [validators.Required()])
    password = TextField('password',  [validators.Required()])
    remember_me = BooleanField('remember_me', default=False)

    def __repr__(self):
        return self.username+" "+self.password


class SignupForm(Form):
    user_name = TextField('user_name',   [
        validators.Length(
            min=4,
            max=15
        ),
        validators.Regexp(
            "^[a-zA-Z0-9]*$",
            message="Username can only contain letters and numbers"
        )
    ])
    first_name = TextField('first_name', [validators.Required()])
    last_name = TextField('last_name', [validators.Required()])
    email = TextField('email', [validators.Required(), validators.Email()])
    password = PasswordField(
        'New Password',
        [validators.Length(min=3, max=10)]
    )
    confirm = PasswordField('Repeat Password', [
        validators.Required(),
        validators.EqualTo('password', message='Passwords must match')
    ])
