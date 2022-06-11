# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from msilib import Table
from tkinter import S
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from apps import db, login_manager

from apps.authentication.util import hash_pass
# from apps.home.routes import lichthi


class Person(db.Model, UserMixin):

    __tablename__ = 'Person'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pcode = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(100))
    xa = db.Column(db.String(100))
    quan = db.Column(db.String(100))
    city = db.Column(db.String(100))
    role = db.Column(db.Integer) # role {'1: Phong Dao tao', '2: Phong Cong tac HSSV', '3: Giang vien', '4: Sinh vien'}

    __mapper_args__ = {
        'polymorphic_on':role,
    }

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def to_dict(self):
        return {
            'id': self.id,
            'pcode': self.pcode,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_birth': self.date_birth.strftime("%Y-%m-%d"),
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'xa': self.xa,
            'quan': self.quan,
            'city': self.city,
            'role': self.role
        }


@login_manager.user_loader
def user_loader(id):
    return Person.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    person = Person.query.filter_by(username=username).first()
    return person if person else None


# -------------------------Nhan vien--------------------------------

class NhanVien(Person):

    __tablename__ = 'NhanVien'

    id = db.Column(db.Integer, ForeignKey(Person.id), primary_key=True)
    type = db.Column(db.Integer)
    
    __mapper_args__ = {
        'polymorphic_identity':1
    }

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_nv': self.pcode,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_birth': self.date_birth.strftime("%Y-%m-%d"),
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'xa': self.xa,
            'quan': self.quan,
            'city': self.city,
            'role': self.role,
            'type': self.type
        }


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
    lichthis = relationship('LichThi', backref='mon', lazy=True, cascade="all, delete-orphan")
    
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

class GiangVien(Person):

    __tablename__ = 'GiangVien'

    id = db.Column(db.Integer, ForeignKey(Person.id), primary_key=True)
    bomon_id = db.Column(db.Integer, ForeignKey(BoMon.id), nullable=False)
    lcns = relationship('LopChuyenNganh', backref='giangvien', lazy=True, cascade="all, delete-orphan")
    lichlops = relationship('LichLop', backref='giangvien', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity':3
    }
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def to_dict(self):
        return {
            'id': self.id,
            'ma_gv': self.pcode,
            'username': self.username,
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
            'ma_gv': self.giangvien.pcode,
            'gv_first_name': self.giangvien.first_name,
            'gv_last_name': self.giangvien.last_name,
            'svs': [{'sv_id': sv.id, 
                    'ma_sv': sv.pcode, 
                    'first_name': sv.first_name, 
                    'last_name': sv.last_name} for sv in self.svs]
        }



# -------------------------SinhVien--------------------------------

class SinhVien(Person):

    __tablename__ = 'SinhVien'

    id = db.Column(db.Integer, ForeignKey(Person.id), primary_key=True)
    sv_ls = relationship('SinhVien_Lop', backref='sinhvien', lazy=True, cascade="all, delete-orphan")
    sv_lichthis = relationship('SinhVien_LichThi', backref='sinhvien', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity':4
    }
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == 'date_birth':
                value = datetime.strptime(value, '%Y-%m-%d')
            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def to_dict(self):
        bangdiem = []
        for sv_l in self.sv_ls:
            diem = {
                'ma_mon': sv_l.lop.mon.ma_mon, 
                'ten_mon': sv_l.lop.mon.ten_mon, 
                'tinchi': sv_l.lop.mon.tinchi, 
                'diemQT': sv_l.diemQT,
                'diemCK': ''
            }
            bangdiem.append(diem)

        for sv_lichthi in self.sv_lichthis:
            for i in bangdiem:
                if i['ma_mon'] == sv_lichthi.lichthi.mon.ma_mon:
                    if not i['diemCK']:
                        i.update({'diemCK': sv_lichthi.diemCK})
                        break
                    if i['diemCK'] < sv_lichthi.diemCK:
                        i.update({'diemCK': sv_lichthi.diemCK})
                        break
        
        tinchi = 0
        diemTB = 0
        for i in bangdiem:
            tinchi += int(i['tinchi'])
            diemQT = float(i['diemQT']) if i['diemQT'] else 0
            diemCK = float(i['diemCK']) if i['diemCK'] else 0
            diemTB += diemQT*0.3 + diemCK*0.7
        diemTB = diemTB / len(bangdiem)

        return {
            'id': self.id,
            'ma_sv': self.pcode,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_birth': self.date_birth.strftime("%Y-%m-%d"),
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'xa': self.xa,
            'quan': self.quan,
            'city': self.city,
            'tinchi': tinchi,
            'diemTB': diemTB,
            'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }

    def to_dictDiem(self):
        bangdiem = []
        for sv_l in self.sv_ls:
            diem = {
                'ma_mon': sv_l.lop.mon.ma_mon, 
                'ten_mon': sv_l.lop.mon.ten_mon, 
                'tinchi': sv_l.lop.mon.tinchi, 
                'diemQT': sv_l.diemQT,
                'diemCK': ''
            }
            bangdiem.append(diem)

        for sv_lichthi in self.sv_lichthis:
            for i in bangdiem:
                if i['ma_mon'] == sv_lichthi.lichthi.mon.ma_mon:
                    if not i['diemCK']:
                        i.update({'diemCK': sv_lichthi.diemCK})
                        break
                    if i['diemCK'] < sv_lichthi.diemCK:
                        i.update({'diemCK': sv_lichthi.diemCK})
                        break

        return {
            'data': [diem for diem in bangdiem]
        }

    def to_dictDiemCT(self, ky_id):
        bangdiem = []
        for sv_l in self.sv_ls:
            if sv_l.lop.ky_id == ky_id:
                diem = {
                    'ma_mon': sv_l.lop.mon.ma_mon, 
                    'ten_mon': sv_l.lop.mon.ten_mon, 
                    'diemQT': sv_l.diemQT,
                    'diemCK': ''
                }
                bangdiem.append(diem)

        for sv_lichthi in self.sv_lichthis:
            if sv_lichthi.lichthi.ky_id == ky_id:
                checkLap = True
                for i in bangdiem:
                    if i['ma_mon'] == sv_lichthi.lichthi.mon.ma_mon:
                        checkLap = False
                        i.update({'diemCK': sv_lichthi.diemCK})
                        break
                if checkLap:
                    diemQT = ''
                    for sv_l in self.sv_ls:
                        if sv_l.lop.mon.ma_mon == sv_lichthi.lichthi.mon.ma_mon:
                            diemQT = sv_l.diemQT
                            break

                    diem = {
                        'ma_mon': sv_lichthi.lichthi.mon.ma_mon, 
                        'ten_mon': sv_lichthi.lichthi.mon.ten_mon, 
                        'diemQT': diemQT,
                        'diemCK': sv_lichthi.diemCK
                    }
                    bangdiem.append(diem)
                

        return {
            'data': [diem for diem in bangdiem]
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

    dkh_start = db.Column(db.DateTime)
    dkh_end = db.Column(db.DateTime)

    dkt_start = db.Column(db.DateTime)
    dkt_end = db.Column(db.DateTime)

    nam_id = db.Column(db.Integer, ForeignKey(Nam.id), nullable=False)
    lops = relationship('Lop', backref='ky', lazy=True, cascade="all, delete-orphan")
    lichthis = relationship('LichThi', backref='ky', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property=='date_start':
                value = datetime.strptime(value, '%Y-%m-%d')
            if property=='dkh_start' or property=='dkh_end' or property=='dkt_start' or property=='dkt_end':
                if value:
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M')
                else:
                    value = None

            setattr(self, property, value)

    def to_dict(self):
        hk1 = Ky.query.filter(Ky.nam_id == self.nam_id, Ky.ten_ky == 1).first()
        dkh_start = self.dkh_start.strftime("%Y-%m-%dT%H:%M") if self.dkh_start else None
        dkh_end = self.dkh_end.strftime("%Y-%m-%dT%H:%M") if self.dkh_end else None
        dkt_start = self.dkt_start.strftime("%Y-%m-%dT%H:%M") if self.dkt_start else None
        dkt_end = self.dkt_end.strftime("%Y-%m-%dT%H:%M") if self.dkt_end else None
        return {
            'id': self.id,
            'ten_ky': self.ten_ky,
            'date_start': self.date_start.strftime("%Y-%m-%d"),
            'dkh_start': dkh_start,
            'dkh_end': dkh_end,
            'dkt_start': dkt_start,
            'dkt_end': dkt_end,
            'nam_id': self.nam_id,
            'hk1': hk1.date_start.strftime("%Y-%m-%d"),
            'date_end': self.nam.date_end.strftime("%Y-%m-%d")
            # 'lcns': [{'lcn_id': lcn.id, 'ten_lcn': lcn.ten_lcn} for lcn in self.lcns]
        }



# -------------------------LopHoc--------------------------------

class Lop(db.Model):

    __tablename__ = 'Lop'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_lop = db.Column(db.String(60), nullable=False)
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
    lichthis = relationship('LichThi', backref='phong', lazy=True, cascade="all, delete-orphan")
    
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
            ma_gv = self.giangvien.pcode
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
            'ma_mon': self.lop.mon.ma_mon,
            'ten_mon': self.lop.mon.ten_mon,
            'sv_id': self.sv_id,
            'ma_sv': self.sinhvien.pcode,
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



# -------------------------LichThi--------------------------------

class LichThi(db.Model):

    __tablename__ = 'LichThi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    mon_id = db.Column(db.Integer, ForeignKey(Mon.id), nullable=False)
    phong_id = db.Column(db.Integer, ForeignKey(Phong.id))
    ky_id = db.Column(db.Integer, ForeignKey(Ky.id), nullable=False)
    sv_lichthis = relationship('SinhVien_LichThi', backref='lichthi', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if property == 'date':
                value = datetime.strptime(value, '%Y-%m-%d')

            setattr(self, property, value)

    def to_dict(self):
        ten_phong = ''
        so_luong = ''
        if self.phong_id != '':
            ten_phong = self.phong.ten_phong
            so_luong = self.phong.so_luong
        return {
            'id': self.id,
            'date': self.date.strftime("%Y-%m-%d"),
            'start': self.start,
            'end': self.end,
            'mon_id': self.mon_id,
            'ma_mon': self.mon.ma_mon,
            'ten_mon': self.mon.ten_mon,
            'tinchi': self.mon.tinchi,
            'phong_id': self.phong_id,
            'ten_phong': ten_phong,
            'so_luong': so_luong,
            'ky_id': self.ky_id,
            'ky': self.ky.ten_ky,
            'nam_id': self.ky.nam_id,
            'sv_lichthis': [{'sv_id': sv_lichthi.sv_id, 'ma_sv': sv_lichthi.sinhvien.pcode, 'first_name': sv_lichthi.sinhvien.first_name, 'last_name': sv_lichthi.sinhvien.last_name} for sv_lichthi in self.sv_lichthis]
        }



# -------------------------SinhVien_Thi--------------------------------

class SinhVien_LichThi(db.Model):

    __tablename__ = 'SinhVien_LichThi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diemCK = db.Column(db.Float)
    lichthi_id = db.Column(db.Integer, ForeignKey(LichThi.id), nullable=False)
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
            'diemCK': self.diemCK,
            'lichthi_id': self.lichthi_id,
            'ma_mon': self.lichthi.mon.ma_mon,
            'ten_mon': self.lichthi.mon.ten_mon,
            'sv_id': self.sv_id,
            'ma_sv': self.sinhvien.pcode,
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

