# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import date
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Email, DataRequired, InputRequired
from apps.authentication.models import Khoa
from apps import db, login_manager

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    # photo = FileField('Your photo', validators=[
    #     FileRequired(),
    #     FileAllowed(['jpg', 'png', 'jpeg', 'JPEG'], 'Images only!')
    # ])
    # #{'user', 'docter', 'worker', 'teacher'}
    # role = SelectField('Role',
    #                          id='role_create',
    #                          choices=[('user', 'user'), 
    #                          ('docter', 'docter'),
    #                          ('worker', 'worker'),
    #                          ('teacher', 'teacher'),
    #                          ])



#----------------------------------Khoa----------------------------------

class CreateKhoaForm(FlaskForm):
    ma_khoa = StringField('Mã khoa',
                         id='ma_khoa',
                         validators=[DataRequired()])
    ten_khoa = StringField('Tên khoa',
                         id='ten_khoa',
                         validators=[DataRequired()])
    phone = StringField('Số điện thoại',
                         id='phone',
                         validators=[DataRequired()])
    email = StringField('Email',
                         id='email',
                         validators=[DataRequired(), Email()])
                         

#----------------------------------Nganh----------------------------------

class CreateNganhForm(FlaskForm):
    ma_nganh = StringField('Mã ngành',
                         id='ma_nganh',
                         validators=[DataRequired()])
    ten_nganh = StringField('Tên ngành',
                         id='ten_nganh',
                         validators=[DataRequired()])
    khoa_id = SelectField('Khoa',
                        id='khoa_id')


#----------------------------------Mon----------------------------------

class CreateMonForm(FlaskForm):
    ma_mon = StringField('Mã môn',
                         id='ma_mon',
                         validators=[DataRequired()])
    ten_mon = StringField('Tên môn',
                         id='ten_mon',
                         validators=[DataRequired()])
    nganh_id = SelectField('Ngành',
                        id='nganh_id')


#----------------------------------ChuongTrinhDaoTao----------------------------------

class CreateChuongTrinhDaoTaoForm(FlaskForm):
    ma_ctdt = StringField('Mã chương trình đào tạo',
                         id='ma_ctdt',
                         validators=[DataRequired()])
    ten_ctdt = StringField('Tên chương trình đào tạo',
                         id='ten_ctdt',
                         validators=[DataRequired()])
    nganh_id = SelectField('Ngành',
                        id='nganh_id')
    mon_id = SelectMultipleField('Môn',
                        id='mon_id')


# #----------------------------------Teacher----------------------------------

# class CreateTeacherForm(FlaskForm):
#     teacher_code = TextField('Mã giảng viên',
#                          id='teacher_code',
#                          validators=[DataRequired()])
#     first_name = TextField('Tên',
#                          id='first_name',
#                          validators=[DataRequired()])
#     last_name = TextField('Họ đệm',
#                          id='last_name',
#                          validators=[DataRequired()])
#     date_birth = DateField('Ngày sinh',
#                          id='date_birth',
#                          format='%d-%m-%Y',
#                          validators=[DataRequired()])
#     address = TextField('Địa chỉ cụ thể',
#                          id='address',
#                          validators=[DataRequired()])
#     xa = TextField('Phường/Xã',
#                          id='xa',
#                          validators=[DataRequired()])
#     quan = TextField('Quận/Huyện',
#                          id='quan',
#                          validators=[DataRequired()])
#     city = TextField('Tỉnh/Thành phố',
#                          id='city',
#                          validators=[DataRequired()])
#     email = TextField('Email',
#                       id='email',
#                       validators=[DataRequired(), Email()])
#     phone = TextField('Số điện thoại',
#                       id='phone',
#                       validators=[DataRequired()])

# #----------------------------------Weekday----------------------------------

# class CreateWeekdayForm(FlaskForm):
#     name = TextField('Buổi học',
#                          id='name',
#                          validators=[DataRequired()])

# #----------------------------------Category----------------------------------

# class CreateCategoryForm(FlaskForm):
#     name = TextField('Bộ môn',
#                          id='name',
#                          validators=[DataRequired()])


# #----------------------------------Course----------------------------------

# class CreateCourseForm(FlaskForm):
#     course_name = TextField('Môn học',
#                         id='course_name',
#                         validators=[DataRequired()])
#     category_id = SelectField('Bộ môn',
#                         id='category_id')


# #----------------------------------Class----------------------------------

# class CreateClassForm(FlaskForm):
#     lesson = TextField('Lớp học',
#                         id='lesson',
#                         validators=[DataRequired()])
#     start_date = DateField('Thời gian bắt đầu',
#                         id='start_date',
#                         format='%d-%m-%Y',
#                         validators=[DataRequired()])
#     end_date = DateField('Thời gian kết thúc',
#                         id='end_date',
#                         format='%d-%m-%Y',
#                         validators=[DataRequired()])
#     teacher_id = SelectField('Giảng viên',
#                         id='teacher_id')
#     course_id = SelectField('Môn học',
#                         id='course_id')


# #----------------------------------ClassStudent----------------------------------

# class CreateClassStudentForm(FlaskForm):
#     class_id = SelectField('Lớp học',
#                         id='class_id')
#     student_id = SelectField('Sinh viên',
#                         id='student_id')
    

# #----------------------------------ClassWeekday----------------------------------

# class CreateClassWeekdayForm(FlaskForm):
#     class_id = SelectField('Lớp học',
#                         id='class_id')
#     weekday_id = SelectField('Buổi học',
#                         id='weekday_id')
#     hours = TextField('Số giờ học',
#                         id='hours',
#                         validators=[DataRequired()])

# #----------------------------------ATTENDANCE----------------------------------

# class CreateAttendanceForm(FlaskForm):
#     status = TextField('Trạng thái',
#                         id='status',
#                         validators=[DataRequired()])
#     class_id = SelectField('Lớp học',
#                         id='class_id')
#     weekday_id = SelectField('Buổi học',
#                         id='weekday_id')
#     student_id = SelectField('Sinh viên',
#                         id='student_id')
    