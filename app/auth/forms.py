# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'保持登录状态')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能由字母，数字，英文句点和下划线组成')])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入不匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该电子邮箱已被使用.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被使用.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入不匹配')])
    password2 = PasswordField(u'确认新密码', validators=[Required()])
    submit = SubmitField(u'更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'重设密码')


class PasswordResetForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入不匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知的邮箱地址.')


class ChangeEmailForm(FlaskForm):
    email = StringField(u'新电子邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'更新电子邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该电子邮箱已被使用.')
