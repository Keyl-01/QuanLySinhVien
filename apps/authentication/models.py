# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from msilib import Table
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    # photo = db.Column(db.String)
    # role = db.Column(db.String(64), default='user') ## role {'user', 'docter', 'worker', 'teacher'}

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


# -------------------------KHOA--------------------------------

class Khoa(db.Model):

    __tablename__ = 'Khoa'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_khoa = db.Column(db.String(30), unique=True, nullable=False)
    ten_khoa = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    nganhs = relationship('Nganh', backref='khoa', lazy=True, cascade="all, delete-orphan")
    bomons = relationship('BoMon', backref='khoa', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
                
            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_khoa': self.ma_khoa,
            'ten_khoa': self.ten_khoa,
            'phone': self.phone,
            'email': self.email
        }


# -------------------------Nganh--------------------------------

class Nganh(db.Model):

    __tablename__ = 'Nganh'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_nganh = db.Column(db.String(30), unique=True, nullable=False)
    ten_nganh = db.Column(db.String(100), unique=True, nullable=False)
    khoa_id = db.Column(db.Integer, ForeignKey(Khoa.id), nullable=False)
    ctdts = relationship('ChuongTrinhDaoTao', backref='nganh', lazy=True, cascade="all, delete-orphan")

    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
                
            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_nganh': self.ma_nganh,
            'ten_nganh': self.ten_nganh,
            'khoa_id': self.khoa_id,
            'ten_khoa': self.khoa.ten_khoa
        }
    

# -------------------------BoMon--------------------------------

class BoMon(db.Model):

    __tablename__ = 'BoMon'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_bomon = db.Column(db.String(30), unique=True, nullable=False)
    ten_bomon = db.Column(db.String(100), unique=True, nullable=False)
    khoa_id = db.Column(db.Integer, ForeignKey(Khoa.id), nullable=False)
    mons = relationship('Mon', backref='bomon', lazy=True, cascade="all, delete-orphan")
    gvs = relationship('GiangVien', backref='bomon', lazy=True, cascade="all, delete-orphan")

    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
                
            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_bomon': self.ma_bomon,
            'ten_bomon': self.ten_bomon,
            'khoa_id': self.khoa_id,
            'ten_khoa': self.khoa.ten_khoa
        }
    


# -------------------------ChuongTrinhDaoTao_MonHoc--------------------------------

ChuongTrinhDaoTao_MonHoc = db.Table('ChuongTrinhDaoTao_MonHoc',
                            Column('ctdt_id', Integer, ForeignKey('ChuongTrinhDaoTao.id'), primary_key=True),
                            Column('mon_id', Integer, ForeignKey('Mon.id'), primary_key=True)
                            )


# -------------------------Monhoc--------------------------------

class Mon(db.Model):

    __tablename__ = 'Mon'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_mon = db.Column(db.String(30), unique=True, nullable=False)
    ten_mon = db.Column(db.String(100), unique=True, nullable=False)
    tinchi = db.Column(db.Integer, nullable=False)
    bomon_id = db.Column(db.Integer, ForeignKey(BoMon.id), nullable=False)
    lops = relationship('Lop', backref='mon', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
                
            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_mon': self.ma_mon,
            'ten_mon': self.ten_mon,
            'tinchi': self.tinchi,
            'bomon_id': self.bomon_id,
            'ten_bomon': self.bomon.ten_bomon
        }
    

# -------------------------ChuongTrinhDaoTao--------------------------------

class ChuongTrinhDaoTao(db.Model):

    __tablename__ = 'ChuongTrinhDaoTao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_ctdt = db.Column(db.String(30), unique=True, nullable=False)
    ten_ctdt = db.Column(db.String(100), unique=True, nullable=False)
    nganh_id = db.Column(db.Integer, ForeignKey(Nganh.id), nullable=False)
    lcns = relationship('LopChuyenNganh', backref='ctdt', lazy=True, cascade="all, delete-orphan")
    mons = relationship('Mon', secondary='ChuongTrinhDaoTao_MonHoc', lazy='subquery', 
                        backref=backref('ctdts', lazy=True))

    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_ctdt': self.ma_ctdt,
            'ten_ctdt': self.ten_ctdt,
            'nganh_id': self.nganh_id,
            'ten_nganh': self.nganh.ten_nganh,
            'mons': [{'mon_id': mon.id, 'ten_mon': mon.ten_mon} for mon in self.mons]
            # 'mon_id': self.mons
            # 'mon_id': self.mons.id,
            # 'ten_mon': self.mons.ten_mon
        }
    

# -------------------------GiangVien--------------------------------

class GiangVien(db.Model):

    __tablename__ = 'GiangVien'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_gv = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(100))
    xa = db.Column(db.String(100))
    quan = db.Column(db.String(100))
    city = db.Column(db.String(100))
    bomon_id = db.Column(db.Integer, ForeignKey(BoMon.id), nullable=False)
    lcns = relationship('LopChuyenNganh', backref='giangvien', lazy=True, cascade="all, delete-orphan")
    lichlops = relationship('LichLop', backref='giangvien', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_gv': self.ma_gv,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_birth': self.date_birth.strftime("%Y-%m-%d"),
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'xa': self.xa,
            'quan': self.quan,
            'city': self.city,
            'bomon_id': self.bomon_id,
            'ten_bomon': self.bomon.ten_bomon
            # 'mons': [{'mon_id': mon.id, 'ten_mon': mon.ten_mon} for mon in self.mons]
        }



# -------------------------LopChuyenNganh_SinhVien--------------------------------

LopChuyenNganh_SinhVien = db.Table('LopChuyenNganh_SinhVien',
                            Column('lcn_id', Integer, ForeignKey('LopChuyenNganh.id'), primary_key=True),
                            Column('sv_id', Integer, ForeignKey('SinhVien.id'), primary_key=True)
                            )



# -------------------------LopChuyenNganh--------------------------------

class LopChuyenNganh(db.Model):

    __tablename__ = 'LopChuyenNganh'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_lcn = db.Column(db.String(30), unique=True, nullable=False)
    ctdt_id = db.Column(db.Integer, ForeignKey(ChuongTrinhDaoTao.id), nullable=False)
    gv_id = db.Column(db.Integer, ForeignKey(GiangVien.id), nullable=False)
    svs = relationship('SinhVien', secondary='LopChuyenNganh_SinhVien', lazy='subquery', 
                        backref=backref('lcns', lazy=True))
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ten_lcn': self.ten_lcn,
            'ctdt_id': self.ctdt_id,
            'ten_ctdt': self.ctdt.ten_ctdt,
            'gv_id': self.gv_id,
            'ma_gv': self.giangvien.ma_gv,
            'gv_first_name': self.giangvien.first_name,
            'gv_last_name': self.giangvien.last_name,
            'svs': [{'sv_id': sv.id, 
                    'ma_sv': sv.ma_sv, 
                    'first_name': sv.first_name, 
                    'last_name': sv.last_name} for sv in self.svs]
        }



# -------------------------SinhVien--------------------------------

class SinhVien(db.Model):

    __tablename__ = 'SinhVien'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_sv = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(100))
    xa = db.Column(db.String(100))
    quan = db.Column(db.String(100))
    city = db.Column(db.String(100))
    sv_ls = relationship('SinhVien_Lop', backref='sinhvien', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_sv': self.ma_sv,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_birth': self.date_birth.strftime("%Y-%m-%d"),
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'xa': self.xa,
            'quan': self.quan,
            'city': self.city,
            'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }



# -------------------------NamHoc--------------------------------

class Nam(db.Model):

    __tablename__ = 'Nam'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_end = db.Column(db.Date, nullable=False)
    kys = relationship('Ky', backref='nam', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_end':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'kys': [{'id': ky.id, 'ten_ky': ky.ten_ky, 'date_start': ky.date_start.strftime("%Y-%m-%d")} for ky in self.kys],
            'date_end': self.date_end.strftime("%Y-%m-%d")
            # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }



# -------------------------KyHoc--------------------------------

class Ky(db.Model):

    __tablename__ = 'Ky'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_ky = db.Column(db.Integer, nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    nam_id = db.Column(db.Integer, ForeignKey(Nam.id), nullable=False)
    lops = relationship('Lop', backref='ky', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_start':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ten_ky': self.ten_ky,
            'date_start': self.date_start.strftime("%Y-%m-%d"),
            'nam_id': self.nam_id,
            'date_end': self.nam.date_end.strftime("%Y-%m-%d")
            # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }



# -------------------------LopHoc--------------------------------

class Lop(db.Model):

    __tablename__ = 'Lop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_lop = db.Column(db.String(60), unique=True, nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    mon_id = db.Column(db.Integer, ForeignKey(Mon.id), nullable=False)
    ky_id = db.Column(db.Integer, ForeignKey(Ky.id), nullable=False)
    lichlops = relationship('LichLop', backref='lop', lazy=True, cascade="all, delete-orphan")
    sv_ls = relationship('SinhVien_Lop', backref='lop', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ten_lop': self.ten_lop,
            'so_luong': self.so_luong,
            'mon_id': self.mon_id,
            'ma_mon': self.mon.ma_mon,
            'ten_mon': self.mon.ten_mon,
            'ky_id': self.ky_id,
            'ky': self.ky.ten_ky,
            'nam_id': self.ky.nam_id
            # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }



# -------------------------PhongHoc--------------------------------

class Phong(db.Model):

    __tablename__ = 'Phong'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_phong = db.Column(db.String(30), unique=True, nullable=False)
    so_luong = db.Column(db.Integer)
    lichlops = relationship('LichLop', backref='phong', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'ten_phong': self.ten_phong,
            'so_luong': self.so_luong
            # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }



# -------------------------LichLop--------------------------------

class LichLop(db.Model):

    __tablename__ = 'LichLop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    thu = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Integer, nullable=False)
    end = db.Column(db.Integer, nullable=False)
    lop_id = db.Column(db.Integer, ForeignKey(Lop.id), nullable=False)
    phong_id = db.Column(db.Integer, ForeignKey(Phong.id), nullable=False)
    gv_id = db.Column(db.Integer, ForeignKey(GiangVien.id))
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        ma_gv = ''
        gv_first_name = ''
        gv_last_name = ''
        if self.gv_id != '':
            ma_gv = self.giangvien.ma_gv
            gv_first_name = self.giangvien.first_name
            gv_last_name = self.giangvien.last_name
        return {
            'id': self.id,
            'thu': self.thu,
            'start': self.start,
            'end': self.end,
            'gv_id': self.gv_id,
            'ma_gv': ma_gv,
            'gv_first_name': gv_first_name,
            'gv_last_name': gv_last_name,
            'lop_id': self.lop_id,
            'ten_lop': self.lop.ten_lop,
            'ma_mon': self.lop.mon.ma_mon,
            'ten_mon': self.lop.mon.ten_mon,
            'tinchi': self.lop.mon.tinchi,
            'phong_id': self.phong_id,
            'ten_phong': self.phong.ten_phong,
            'so_luong': self.phong.so_luong
            # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }



# -------------------------SinhVien_LopHoc--------------------------------

class SinhVien_Lop(db.Model):

    __tablename__ = 'SinhVien_Lop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diemQT = db.Column(db.Float)
    lop_id = db.Column(db.Integer, ForeignKey(Lop.id), nullable=False)
    sv_id = db.Column(db.Integer, ForeignKey(SinhVien.id), nullable=False)
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        return {
            'id': self.id,
            'diemQT': self.diemQT,
            'lop_id': self.lop_id,
            'ten_lop': self.lop.ten_lop,
            'sv_id': self.sv_id,
            'ma_sv': self.sinhvien.ma_sv,
            'sv_first_name': self.sinhvien.first_name,
            'sv_last_name': self.sinhvien.last_name,
            'date_birth': self.sinhvien.date_birth.strftime("%Y-%m-%d"),
            'email': self.sinhvien.email,
            'phone': self.sinhvien.phone,
            'address': self.sinhvien.address,
            'xa': self.sinhvien.xa,
            'quan': self.sinhvien.quan,
            'city': self.sinhvien.city,
            'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.sinhvien.lcns]
            # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }






# -------------------------CaHoc--------------------------------

# class Ca(db.Model):

#     __tablename__ = 'Ca'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ca = db.Column(db.String(30), unique=True, nullable=False)
#     start = db.Column(db.DateTime, unique=True, nullable=False)
#     end = db.Column(db.DateTime, unique=True, nullable=False)
    
#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if property=='start' or property=='end':
#                 value = datetime.strptime(value, '%Y-%m-%d')

#             setattr(self, property, value)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'ten_phong': self.ten_phong,
#             'so_luong': self.so_luong
#             # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
#         }



# # -------------------------STUDENT--------------------------------

# class Student(db.Model):

#     __tablename__ = 'student'

#     id = db.Column(db.Integer, primary_key=True)
#     student_code = db.Column(db.String(30), unique=True, nullable=False)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     date_birth = db.Column(db.Date)
#     address = db.Column(db.String(100))
#     xa = db.Column(db.String(100))
#     quan = db.Column(db.String(100))
#     city = db.Column(db.String(100))
#     email = db.Column(db.String(64), nullable=False)
#     phone = db.Column(db.String(64), nullable=False)
    
#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if property == 'date_birth':
#                 value = datetime.strptime(value, '%Y-%m-%d')
                
#             setattr(self, property, value)

# # -------------------------TEACHER--------------------------------

# class Teacher(db.Model):

#     __tablename__ = 'teacher'

#     id = db.Column(db.Integer, primary_key=True)
#     teacher_code = db.Column(db.String(30), unique=True, nullable=False)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     date_birth = db.Column(db.Date)
#     address = db.Column(db.String(100))
#     xa = db.Column(db.String(100))
#     quan = db.Column(db.String(100))
#     city = db.Column(db.String(100))
#     email = db.Column(db.String(64), nullable=False)
#     phone = db.Column(db.String(64), nullable=False)
    
#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if property == 'date_birth':
#                 value = datetime.strptime(value, '%Y-%m-%d')

#             setattr(self, property, value)

# # -------------------------CATEGORY--------------------------------

# class Category(db.Model):

#     __tablename__ = 'category'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(600), unique=True)

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)

#             setattr(self, property, value)

# # -------------------------COURSE--------------------------------

# class Course(db.Model):

#     __tablename__ = 'course'

#     id = db.Column(db.Integer, primary_key=True)
#     course_name = db.Column(db.String(600))
#     category_id = db.Column(db.Integer, ForeignKey(Category.id), nullable=False)

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)

#             setattr(self, property, value)

# # -------------------------WEEKDAY--------------------------------

# class Weekday(db.Model):

#     __tablename__ = 'weekday'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(600))

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)

#             setattr(self, property, value)

# # -------------------------CLASS--------------------------------

# class Class(db.Model):

#     __tablename__ = 'class'

#     id = db.Column(db.Integer, primary_key=True)
#     lesson = db.Column(db.String(600), unique=True)
#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)
#     teacher_id = db.Column(db.Integer, ForeignKey(Teacher.id), nullable=False)
#     course_id = db.Column(db.Integer, ForeignKey(Course.id), nullable=False)

    
#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if property=='start_date' or property=='end_date':
#                 value = datetime.strptime(value, '%Y-%m-%d')

#             setattr(self, property, value)

# # -------------------------CLASS_STUDENT--------------------------------

# class ClassStudent(db.Model):

#     __tablename__ = 'class_student'

#     id = db.Column(db.Integer, primary_key=True)
#     class_id = db.Column(db.Integer, ForeignKey(Class.id), nullable=False)
#     student_id = db.Column(db.Integer, ForeignKey(Student.id), nullable=False)
    
#     PrimaryKeyConstraint('class_id', 'student_id')
    
#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             setattr(self, property, value)

# # -------------------------CLASS_WEEKDAY--------------------------------

# class ClassWeekday(db.Model):

#     __tablename__ = 'class_weekday'

#     id = db.Column(db.Integer, primary_key=True)
#     class_id = db.Column(db.Integer, ForeignKey(Class.id), nullable=False)
#     weekday_id = db.Column(db.Integer, ForeignKey(Weekday.id), nullable=False)
#     hours = db.Column(db.String(600))
    
#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             setattr(self, property, value)

# # -------------------------ATTENDANCE--------------------------------

# class Attendance(db.Model):

#     __tablename__ = 'attendance'

#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.String(600))
#     class_id = db.Column(db.Integer, ForeignKey(Class.id), nullable=False)
#     weekday_id = db.Column(db.Integer, ForeignKey(Weekday.id), nullable=False)
#     student_id = db.Column(db.Integer, ForeignKey(Student.id), nullable=False)

    
#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             setattr(self, property, value)

#     def __init__(self, status, class_id, weekday_id, student_id):
#         self.status = status
#         self.class_id = class_id
#         self.weekday_id = weekday_id
#         self.student_id = student_id
