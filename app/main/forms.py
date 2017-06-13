# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateTimeField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from datetime import datetime


class NameForm(FlaskForm):
    name = StringField(u'您的名字是？', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能由字母，数字，英文句点和下划线组成')])
    confirmed = BooleanField(u'已确认')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人简介')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该电子邮箱已被使用.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被使用.')


class PostForm(FlaskForm):
    date = DateTimeField(u'时间', format='%Y/%m/%d %H:%M')
    location = StringField(u'去哪儿?', validators=[Required()])
    body = PageDownField(u"做什么?", validators=[Required()])
    submit = SubmitField(u'提交')


class CommentForm(FlaskForm):
    body = StringField(u'输入您想说的话', validators=[Required()])
    submit = SubmitField(u'提交')
