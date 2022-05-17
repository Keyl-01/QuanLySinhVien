# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import date
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, IntegerField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Email, DataRequired, NumberRange, InputRequired
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


#----------------------------------BoMon----------------------------------

class CreateBoMonForm(FlaskForm):
    ma_bomon = StringField('Mã bộ môn',
                         id='ma_bomon',
                         validators=[DataRequired()])
    ten_bomon = StringField('Tên bộ môn',
                         id='ten_bomon',
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
    tinchi = IntegerField('Tín chỉ',
                         id='tinchi',
                         validators=[DataRequired(), NumberRange(min=0, max=10)])
    bomon_id = SelectField('Bộ môn',
                        id='bomon_id')



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
    mon_id = SelectMultipleField('Môn học',
                        id='mon_id')


#----------------------------------GiangVien----------------------------------

class CreateGiangVienForm(FlaskForm):
    ma_gv = StringField('Mã giảng viên',
                         id='ma_gv',
                         validators=[DataRequired()])
    first_name = StringField('Tên',
                         id='first_name',
                         validators=[DataRequired()])
    last_name = StringField('Họ đệm',
                         id='last_name',
                         validators=[DataRequired()])
    date_birth = DateField('Ngày sinh',
                         id='date_birth',
                         format='%d-%m-%Y',
                         validators=[DataRequired()])
    address = StringField('Địa chỉ cụ thể',
                         id='address',
                         validators=[DataRequired()])
    xa = StringField('Phường/Xã',
                         id='xa',
                         validators=[DataRequired()])
    quan = StringField('Quận/Huyện',
                         id='quan',
                         validators=[DataRequired()])
    city = StringField('Tỉnh/Thành phố',
                         id='city',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email',
                      validators=[DataRequired(), Email()])
    phone = StringField('Số điện thoại',
                      id='phone',
                      validators=[DataRequired()])
    bomon_id = SelectField('Bộ môn',
                        id='bomon_id')


#----------------------------------LopChuyenNganh----------------------------------

class CreateLopChuyenNganhForm(FlaskForm):
    ten_lcn = StringField('Tên lớp chuyên ngành',
                         id='ten_lcn',
                         validators=[DataRequired()])
    ctdt_id = SelectField('Chương trình đào tạo',
                        id='ctdt_id')
    gv_id = SelectField('Giáo viên chủ nhiệm',
                        id='gv_id')
    sv_id = SelectMultipleField('Sinh viên',
                        id='sv_id')


#----------------------------------SinhVien----------------------------------

class CreateSinhVienForm(FlaskForm):
    ma_sv = StringField('Mã sinh viên',
                         id='ma_sv',
                         validators=[DataRequired()])
    first_name = StringField('Tên',
                         id='first_name',
                         validators=[DataRequired()])
    last_name = StringField('Họ đệm',
                         id='last_name',
                         validators=[DataRequired()])
    date_birth = DateField('Ngày sinh',
                         id='date_birth',
                         format='%d-%m-%Y',
                         validators=[DataRequired()])
    address = StringField('Địa chỉ cụ thể',
                         id='address',
                         validators=[DataRequired()])
    xa = StringField('Phường/Xã',
                         id='xa',
                         validators=[DataRequired()])
    quan = StringField('Quận/Huyện',
                         id='quan',
                         validators=[DataRequired()])
    city = StringField('Tỉnh/Thành phố',
                         id='city',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email',
                      validators=[DataRequired(), Email()])
    phone = StringField('Số điện thoại',
                      id='phone',
                      validators=[DataRequired()])
    lcn_id = SelectMultipleField('Lớp chuyên ngành',
                        id='lcn_id')


#----------------------------------LopHoc----------------------------------

class CreateLopForm(FlaskForm):
    ten_lop = StringField('Tên lớp',
                         id='ten_lop',
                         validators=[DataRequired()])
    # so_luong = IntegerField('Sức chứa tối đa',
    #                      id='so_luong',
    #                      validators=[DataRequired(), NumberRange(min=0, max=9999)])
    so_luong = StringField('Sức chứa tối đa',
                         id='so_luong',
                         validators=[DataRequired()])
    mon_id = SelectField('Môn học',
                        id='mon_id')


#----------------------------------PhongHoc----------------------------------

class CreatePhongForm(FlaskForm):
    ten_phong = StringField('Tên phòng',
                         id='ten_phong',
                         validators=[DataRequired()])
    so_luong = StringField('Sức chứa',
                         id='so_luong',
                         validators=[DataRequired()])

                
#----------------------------------LichLop----------------------------------

class CreateLichLopForm(FlaskForm):
    lop_id = SelectField('Lớp',
                         id='lop_id',
                         validators=[DataRequired()])
    thu = SelectField('Thứ',
                         id='thu',
                         validators=[DataRequired()],
                         choices=[('1', 'Không xác định'), ('2', 'Thứ 2'), ('3', 'Thứ 3'), ('4', 'Thứ 4'), ('5', 'Thứ 5'), ('6', 'Thứ 6'), ('7', 'Thứ 7'), ('8', 'Chủ nhật')])
    start = SelectField('Ca bắt đầu',
                         id='start',
                         validators=[DataRequired()],
                         choices=[('1', 'Ca 1'), ('2', 'Ca 2'), ('3', 'Ca 3'), ('4', 'Ca 4'), ('5', 'Ca 5'), ('6', 'Ca 6'), ('7', 'Ca 7'), 
                                ('8', 'Ca 8'), ('9', 'Ca 9'), ('10', 'Ca 10'), ('11', 'Ca 11'), ('12', 'Ca 12'), ('13', 'Ca 13'), ('14', 'Ca 14')])
    end = SelectField('Ca kết thúc',
                         id='end',
                         validators=[DataRequired()],
                         choices=[('1', 'Ca 1'), ('2', 'Ca 2'), ('3', 'Ca 3'), ('4', 'Ca 4'), ('5', 'Ca 5'), ('6', 'Ca 6'), ('7', 'Ca 7'), 
                                ('8', 'Ca 8'), ('9', 'Ca 9'), ('10', 'Ca 10'), ('11', 'Ca 11'), ('12', 'Ca 12'), ('13', 'Ca 13'), ('14', 'Ca 14')])
    gv_id = SelectField('Giảng viên giảng dạy',
                        id='gv_id',
                        validators=[DataRequired()])
    phong_id = SelectField('Phòng',
                         id='phong_id',
                         validators=[DataRequired()])


#----------------------------------SinhVien_LopHoc----------------------------------

class CreateSinhVien_LopForm(FlaskForm):
    lop_id = SelectField('Lớp',
                         id='lopsv_id',
                         validators=[DataRequired()])
    sv_id = SelectField('Sinh viên',
                        id='sv_id',
                        validators=[DataRequired()])
    diemQT = StringField('Điểm quá trình',
                         id='diemQT',
                         validators=[DataRequired()])


# #----------------------------------Teacher----------------------------------

# class CreateTeacherForm(FlaskForm):
#     teacher_code = StringField('Mã giảng viên',
#                          id='teacher_code',
#                          validators=[DataRequired()])
#     first_name = StringField('Tên',
#                          id='first_name',
#                          validators=[DataRequired()])
#     last_name = StringField('Họ đệm',
#                          id='last_name',
#                          validators=[DataRequired()])
#     date_birth = DateField('Ngày sinh',
#                          id='date_birth',
#                          format='%d-%m-%Y',
#                          validators=[DataRequired()])
#     address = StringField('Địa chỉ cụ thể',
#                          id='address',
#                          validators=[DataRequired()])
#     xa = StringField('Phường/Xã',
#                          id='xa',
#                          validators=[DataRequired()])
#     quan = StringField('Quận/Huyện',
#                          id='quan',
#                          validators=[DataRequired()])
#     city = StringField('Tỉnh/Thành phố',
#                          id='city',
#                          validators=[DataRequired()])
#     email = StringField('Email',
#                       id='email',
#                       validators=[DataRequired(), Email()])
#     phone = StringField('Số điện thoại',
#                       id='phone',
#                       validators=[DataRequired()])

# #----------------------------------Weekday----------------------------------

# class CreateWeekdayForm(FlaskForm):
#     name = StringField('Buổi học',
#                          id='name',
#                          validators=[DataRequired()])

# #----------------------------------Category----------------------------------

# class CreateCategoryForm(FlaskForm):
#     name = StringField('Bộ môn',
#                          id='name',
#                          validators=[DataRequired()])


# #----------------------------------Course----------------------------------

# class CreateCourseForm(FlaskForm):
#     course_name = StringField('Môn học',
#                         id='course_name',
#                         validators=[DataRequired()])
#     category_id = SelectField('Bộ môn',
#                         id='category_id')


# #----------------------------------Class----------------------------------

# class CreateClassForm(FlaskForm):
#     lesson = StringField('Lớp học',
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
#     hours = StringField('Số giờ học',
#                         id='hours',
#                         validators=[DataRequired()])

# #----------------------------------ATTENDANCE----------------------------------

# class CreateAttendanceForm(FlaskForm):
#     status = StringField('Trạng thái',
#                         id='status',
#                         validators=[DataRequired()])
#     class_id = SelectField('Lớp học',
#                         id='class_id')
#     weekday_id = SelectField('Buổi học',
#                         id='weekday_id')
#     student_id = SelectField('Sinh viên',
#                         id='student_id')
    