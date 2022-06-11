# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


import json
from re import S
from sqlalchemy import desc, asc
from apps.authentication.forms import CreateFilterCTDTForm, CreateFilterNamHocForm, CreateTaiKhoanForm, CreateNhanVienForm, CreateKhoaForm, CreateNganhForm, CreateBoMonForm, CreateMonForm, CreateChuongTrinhDaoTaoForm, CreateLopChuyenNganhForm, CreateSinhVienForm, CreateGiangVienForm, CreateLopForm, CreatePhongForm, CreateLichLopForm, CreateSinhVien_LopForm, CreateNamForm, CreateKyForm, CreateLichThiForm, CreateSinhVien_LichThiForm, CreateBangDiemForm
from apps.authentication.models import Khoa, Nganh, BoMon, Mon, ChuongTrinhDaoTao, GiangVien, LopChuyenNganh, SinhVien, Lop, Phong, LichLop, SinhVien_LichThi, SinhVien_Lop, Nam, Ky, LichThi, NhanVien, Person
from apps.authentication.util import verify_pass
from apps.home import blueprint
from apps import db, login_manager, create_app
from flask import Flask, render_template, jsonify, redirect, request, session, url_for, Response
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from sqlalchemy import or_, and_
# import cv2
# import dlib
# import numpy as np
# import os
# from PIL import Image
from datetime import datetime

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

#-------------------------------------Toan truong---------------------------------------------

@blueprint.route('/tkbtruong')
@login_required
def tkbTruong():
    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]
    return render_template('home/tkbtruong.html', segment='tkbtruong', form=create_filter_nam_form)

@blueprint.route('/lichthitruong')
@login_required
def lichThiTruong():
    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]
    return render_template('home/lichthitruong.html', segment='lichthitruong', form=create_filter_nam_form)

@blueprint.route('/chuongtrinhdaotaotruong')
@login_required
def chuongTrinhDaoTaoTruong():
    create_filter_ctdt_form = CreateFilterCTDTForm(request.form)
    khoa =  Khoa.query.all()
    create_filter_ctdt_form.nganh_id.choices = dict([(row.ten_khoa, [(nganh.id, nganh.ten_nganh) for nganh in row.nganhs]) for row in khoa])
    return render_template('home/chuongtrinhdaotaotruong.html', segment='chuongtrinhdaotao', form=create_filter_ctdt_form)




#-------------------------------------Sinh vien---------------------------------------------
#-------------------------------------Thong tin ca nhan------------------------------------------

@blueprint.route('/profilesv')
@login_required
def profileSV():
    create_sv_form = CreateSinhVienForm(request.form)
    return render_template('home/profilesv.html', segment='profilesv', form=create_sv_form)

@blueprint.route('/dangkyhoc')
@login_required
def dangKyHoc():
    return render_template('home/dangkyhoc.html', segment='dangkyhoc')

@blueprint.route('/dangkyhoc', methods=['POST'])
@login_required
def addDKH():
    lop_id = int(request.form['lop_id'])
    sv_id = int(request.form['sv_id'])
    ky_id = int(request.form['ky_id'])

    ky = Ky.query.filter(Ky.dkh_start != None, Ky.dkh_end != None).order_by(asc(Ky.date_start)).first()
    if ky:
        now = datetime.now()
        if now<ky.dkh_start or now>=ky.dkh_end:
            return

    mon_id = (Lop.query.filter_by(id=lop_id).first()).mon_id
    lops = Lop.query.filter(Lop.ky_id == ky_id, Lop.mon_id == mon_id).all()
    for lop in lops:
        sv_lop = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id, SinhVien_Lop.lop_id == lop.id).first()
        if sv_lop:
            if sv_lop is None:
                return jsonify({'duplicate': 'Không tìm thấy.'})
            db.session.delete(sv_lop)
            db.session.commit()

    lichlop1 = LichLop.query.filter(LichLop.lop_id == lop_id).all()
    mon1 = Lop.query.filter(Lop.id == lop_id).first()

    lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id).all()

    for lop in lops:
        mon2 = Lop.query.filter(Lop.mon_id == lop.lop.mon_id).first()
        if mon2 is not None and mon1.mon_id == mon2.mon_id:
            return jsonify({'duplicate': 'Sinh viên này đã đăng ký học phần này. Không thể thêm sinh viên này.'})

    for lop in lops:
        check = Lop.query.filter(Lop.ky_id == ky_id, Lop.id == lop.lop_id).first()
        if check:
            lichlop2 = LichLop.query.filter(LichLop.lop_id == lop.lop_id).all()
            for row2 in lichlop2:
                for row1 in lichlop1:
                    if row2.thu == row1.thu:
                        if((row2.start<=row1.start and row1.start<=row2.end) or (row2.start<=row1.end and row1.end<=row2.end)):
                            return jsonify({'duplicate': 'Sinh viên này bị trùng lịch. Không thể thêm sinh viên này.'})

    sv_lop = SinhVien_Lop(**request.form)
    db.session.add(sv_lop)
    db.session.commit()
        
    return jsonify({'success': 'Đăng ký thành công.'})

@blueprint.route('/dangkyhoc/<int:sv_id>/<int:lop_id>', methods=['DELETE'])
@login_required
def deleteDKH(sv_id, lop_id):
    ky = Ky.query.filter(Ky.dkh_start != None, Ky.dkh_end != None).order_by(asc(Ky.date_start)).first()
    if ky:
        now = datetime.now()
        if now<ky.dkh_start or now>=ky.dkh_end:
            return

    sv_lop = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id, SinhVien_Lop.lop_id == lop_id).first()
    if sv_lop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(sv_lop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})




@blueprint.route('/dangkythilai')
@login_required
def dangKyThiLai():
    return render_template('home/dangkythilai.html', segment='dangkythilai')

@blueprint.route('/dangkythilai', methods=['POST'])
@login_required
def addDKTL():
    lichthi_id = int(request.form['lichthi_id'])
    sv_id = int(request.form['sv_id'])
    ky_id = int(request.form['ky_id'])

    ky = Ky.query.filter(Ky.dkt_start != None, Ky.dkt_end != None).order_by(asc(Ky.date_start)).first()
    if ky:
        now = datetime.now()
        if now<ky.dkt_start or now>=ky.dkt_end:
            return

    mon_id = (Lop.query.filter_by(id=lop_id).first()).mon_id
    lops = Lop.query.filter(Lop.ky_id == ky_id, Lop.mon_id == mon_id).all()
    for lop in lops:
        sv_lop = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id, SinhVien_Lop.lop_id == lop.id).first()
        if sv_lop:
            if sv_lop is None:
                return jsonify({'duplicate': 'Không tìm thấy.'})
            db.session.delete(sv_lop)
            db.session.commit()

    lichlop1 = LichLop.query.filter(LichLop.lop_id == lop_id).all()
    mon1 = Lop.query.filter(Lop.id == lop_id).first()

    lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id).all()

    for lop in lops:
        mon2 = Lop.query.filter(Lop.mon_id == lop.lop.mon_id).first()
        if mon2 is not None and mon1.mon_id == mon2.mon_id:
            return jsonify({'duplicate': 'Sinh viên này đã đăng ký học phần này. Không thể thêm sinh viên này.'})

    for lop in lops:
        check = Lop.query.filter(Lop.ky_id == ky_id, Lop.id == lop.lop_id).first()
        if check:
            lichlop2 = LichLop.query.filter(LichLop.lop_id == lop.lop_id).all()
            for row2 in lichlop2:
                for row1 in lichlop1:
                    if row2.thu == row1.thu:
                        if((row2.start<=row1.start and row1.start<=row2.end) or (row2.start<=row1.end and row1.end<=row2.end)):
                            return jsonify({'duplicate': 'Sinh viên này bị trùng lịch. Không thể thêm sinh viên này.'})

    sv_lop = SinhVien_Lop(**request.form)
    db.session.add(sv_lop)
    db.session.commit()
        
    return jsonify({'success': 'Đăng ký thành công.'})

@blueprint.route('/dangkythilai/<int:sv_id>/<int:lop_id>', methods=['DELETE'])
@login_required
def deleteDKTL(sv_id, lop_id):
    ky = Ky.query.filter(Ky.dkh_start != None, Ky.dkh_end != None).order_by(asc(Ky.date_start)).first()
    if ky:
        now = datetime.now()
        if now<ky.dkh_start or now>=ky.dkh_end:
            return

    sv_lop = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id, SinhVien_Lop.lop_id == lop_id).first()
    if sv_lop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(sv_lop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})




@blueprint.route('/tkbsv')
@login_required
def tkbSV():
    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]
    return render_template('home/tkbsv.html', segment='tkbsv', form=create_filter_nam_form)

@blueprint.route('/bangdiemsv')
@login_required
def bangDiemSV():
    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]
    return render_template('home/bangdiemsv.html', segment='bangdiemsv', form=create_filter_nam_form)

@blueprint.route('/lichthisv')
@login_required
def lichThiSV():
    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]
    return render_template('home/lichthisv.html', segment='lichthisv', form=create_filter_nam_form)


#-------------------------------------Phong Cong tac HSSV---------------------------------------------
#-------------------------------------Thong tin ca nhan------------------------------------------

@blueprint.route('/profilenvhssv')
@login_required
def profileNVHSSV():
    create_nv_form = CreateNhanVienForm(request.form)
    return render_template('home/profilenvhssv.html', segment='profilenvhssv', form=create_nv_form)


#-------------------------------------Giang vien---------------------------------------------
#-------------------------------------Thong tin ca nhan------------------------------------------

@blueprint.route('/profilegv')
@login_required
def profileGV():
    create_gv_form = CreateGiangVienForm(request.form)
    return render_template('home/profilegv.html', segment='profilegv', form=create_gv_form)

@blueprint.route('/tkbgv')
@login_required
def tkbGV():
    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]
    return render_template('home/tkbgv.html', segment='tkbgv', form=create_filter_nam_form)

@blueprint.route('/lopgv')
@login_required
def lopGV():
    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]
    return render_template('home/lopgv.html', segment='lopgv', form=create_filter_nam_form)


#-------------------------------------Phòng Đào tạo---------------------------------------------
#-------------------------------------Thong tin ca nhan------------------------------------------

@blueprint.route('/profilenv')
@login_required
def profileNV():
    create_nv_form = CreateNhanVienForm(request.form)
    return render_template('home/profilenv.html', segment='profilenv', form=create_nv_form)

@blueprint.route('/profilenv/<int:id>', methods=['PUT'])
@login_required
def updateProfileNV(id):
    ma_nv = request.form['ma_nv']
    email = request.form['email']
    phone = request.form['phone']

    found_nv = NhanVien.query.filter_by(id=id).first()

    nv = Person.query.filter(Person.id != id, Person.pcode == ma_nv).first()
    if nv:
        return jsonify({'duplicate': 'Mã nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = Person.query.filter(Person.id != id, Person.email == email).first()
    if nv:
        return jsonify({'duplicate': 'Email của nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = Person.query.filter(Person.id != id, Person.phone == phone).first()
    if nv:
        return jsonify({'duplicate': 'Số điện thoại của nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = NhanVien(**request.form)
    found_nv.pcode = ma_nv
    found_nv.first_name = nv.first_name
    found_nv.last_name = nv.last_name
    found_nv.date_birth = nv.date_birth
    found_nv.address = nv.address
    found_nv.xa = nv.xa
    found_nv.quan = nv.quan
    found_nv.city = nv.city
    found_nv.email = nv.email
    found_nv.phone = nv.phone
    found_nv.type = nv.type

    found_nv.username = ma_nv
    db.session.commit()

    # return redirect(url_for('home_blueprint.profileNV'))
    return jsonify({'success': 'Cập nhật thành công.'})


@blueprint.route('/changepass/<int:id>', methods=['PUT'])
@login_required
def changePassword(id):
    current_password = request.form['current_password']

    found_person = Person.query.filter_by(id=id).first()

    if not verify_pass(current_password, found_person.password):
        return jsonify({'duplicate': 'Mật khẩu hiện tại không đúng. Không thể đổi mật khẩu.'})

    person = Person(**request.form)
    found_person.password = person.password
    db.session.commit()

    # return redirect(url_for('home_blueprint.profileNV'))
    return jsonify({'success': 'Đổi mật khẩu thành công.'})


#-------------------------------------Tài Khoản------------------------------------------

@blueprint.route('/taikhoan')
@login_required
def taiKhoan():
    create_taikhoan_form = CreateTaiKhoanForm(request.form)
    return render_template('home/taikhoan.html', segment='taikhoan', form=create_taikhoan_form)

@blueprint.route('/taikhoan/<int:id>', methods=['PUT'])
@login_required
def updateTaiKhoan(id):
    if 'nhanvien' in request.form:
        found_nv = NhanVien.query.filter_by(id=id).first()
        nv = NhanVien(**request.form)
        found_nv.password = nv.password
        db.session.commit()
        return jsonify({'success': 'Cập nhật thành công.'})

    if 'giangvien' in request.form:
        found_gv = GiangVien.query.filter_by(id=id).first()
        gv = GiangVien(**request.form)
        found_gv.password = gv.password
        db.session.commit()
        return jsonify({'success': 'Cập nhật thành công.'})

    if 'sinhvien' in request.form:
        found_sv = SinhVien.query.filter_by(id=id).first()
        sv = SinhVien(**request.form)
        found_sv.password = sv.password
        db.session.commit()
        return jsonify({'success': 'Cập nhật thành công.'})



#-------------------------------------Nhan Vien------------------------------------------

@blueprint.route('/nhanvien')
@login_required
def nhanVien():
    create_nv_form = CreateNhanVienForm(request.form)
    return render_template('home/nhanvien.html', segment='nhanvien', form=create_nv_form)

@blueprint.route('/nhanvien', methods=['POST'])
@login_required
def addNhanVien():
    ma_nv = request.form['ma_nv']
    email = request.form['email']
    phone = request.form['phone']

    nv = Person.query.filter_by(pcode=ma_nv).first()
    if nv:
        return jsonify({'duplicate': 'Mã nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = Person.query.filter_by(email=email).first()
    if nv:
        return jsonify({'duplicate': 'Email của nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = Person.query.filter_by(phone=phone).first()
    if nv:
        return jsonify({'duplicate': 'Số điện thoại của nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = NhanVien(**request.form)
    nv.pcode = ma_nv
    nv.username = nv.pcode
    db.session.add(nv)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/nhanvien/<int:id>', methods=['PUT'])
@login_required
def updateNhanVien(id):
    ma_nv = request.form['ma_nv']
    email = request.form['email']
    phone = request.form['phone']

    found_nv = NhanVien.query.filter_by(id=id).first()

    nv = Person.query.filter(Person.id != id, Person.pcode == ma_nv).first()
    if nv:
        return jsonify({'duplicate': 'Mã nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = Person.query.filter(Person.id != id, Person.email == email).first()
    if nv:
        return jsonify({'duplicate': 'Email của nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = Person.query.filter(Person.id != id, Person.phone == phone).first()
    if nv:
        return jsonify({'duplicate': 'Số điện thoại của nhân viên đã tồn tại. Không thể lưu nhân viên này.'})

    nv = NhanVien(**request.form)
    # print(nv.first_name)
    found_nv.pcode = ma_nv
    found_nv.first_name = nv.first_name
    found_nv.last_name = nv.last_name
    found_nv.date_birth = nv.date_birth
    found_nv.address = nv.address
    found_nv.xa = nv.xa
    found_nv.quan = nv.quan
    found_nv.city = nv.city
    found_nv.email = nv.email
    found_nv.phone = nv.phone
    found_nv.type = nv.type
    db.session.commit()

    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/nhanvien/<int:id>', methods=['DELETE'])
@login_required
def deleteNhanVien(id):
    nv = NhanVien.query.get_or_404(id)
    if nv is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(nv)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Khoa------------------------------------------

@blueprint.route('/khoa')
@login_required
def khoa():
    create_khoa_form = CreateKhoaForm(request.form)
    return render_template('home/khoa.html', segment='khoa', form=create_khoa_form)

@blueprint.route('/khoa', methods=['POST'])
@login_required
def addKhoa():
    ma_khoa = request.form['ma_khoa']
    ten_khoa = request.form['ten_khoa']

    khoa = Khoa.query.filter_by(ma_khoa=ma_khoa).first()
    if khoa:
        return jsonify({'duplicate': 'Mã khoa đã tồn tại. Không thể lưu khoa này.'})
        # return jsonify({'htmlresponse': render_template('response.html', msg='Mã khoa đã tồn tại. Không thể lưu khoa này')})

    khoa = Khoa.query.filter_by(ten_khoa=ten_khoa).first()
    if khoa:
        return jsonify({'duplicate': 'Tên khoa đã tồn tại. Không thể lưu khoa này.'})

    khoa = Khoa(**request.form)
    db.session.add(khoa)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/khoa/<int:id>', methods=['PUT'])
@login_required
def updateKhoa(id):
    ma_khoa = request.form['ma_khoa']
    ten_khoa = request.form['ten_khoa']

    found_khoa = Khoa.query.filter_by(id=id).first()

    khoa = Khoa.query.filter(Khoa.id != id, Khoa.ma_khoa == ma_khoa).first()
    if khoa:
        return jsonify({'duplicate': 'Mã khoa đã tồn tại. Không thể lưu khoa này.'})

    khoa = Khoa.query.filter(Khoa.id != id, Khoa.ten_khoa == ten_khoa).first()
    if khoa:
        return jsonify({'duplicate': 'Tên khoa đã tồn tại. Không thể lưu khoa này.'})

    khoa = Khoa(**request.form)
    found_khoa.ma_khoa = khoa.ma_khoa
    found_khoa.ten_khoa = khoa.ten_khoa
    found_khoa.phone = khoa.phone
    found_khoa.email = khoa.email
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/khoa/<int:id>', methods=['DELETE'])
@login_required
def deleteKhoa(id):
    khoa = Khoa.query.get_or_404(id)
    if khoa is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(khoa)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Ngành------------------------------------------

@blueprint.route('/nganh')
@login_required
def nganh():
    create_nganh_form = CreateNganhForm(request.form)
    khoa =  Khoa.query.all()
    create_nganh_form.khoa_id.choices = [(row.id, row.ten_khoa) for row in khoa]
    return render_template('home/nganh.html', segment='nganh', form=create_nganh_form)

@blueprint.route('/nganh', methods=['POST'])
@login_required
def addNganh():
    ma_nganh = request.form['ma_nganh']
    ten_nganh = request.form['ten_nganh']

    nganh = Nganh.query.filter_by(ma_nganh=ma_nganh).first()
    if nganh:
        return jsonify({'duplicate': 'Mã ngành đã tồn tại. Không thể lưu ngành này.'})

    nganh = Nganh.query.filter_by(ten_nganh=ten_nganh).first()
    if nganh:
        return jsonify({'duplicate': 'Tên ngành đã tồn tại. Không thể lưu ngành này.'})

    nganh = Nganh(**request.form)
    db.session.add(nganh)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/nganh/<int:id>', methods=['PUT'])
@login_required
def updateNganh(id):
    ma_nganh = request.form['ma_nganh']
    ten_nganh = request.form['ten_nganh']

    found_nganh = Nganh.query.filter_by(id=id).first()

    nganh = Nganh.query.filter(Nganh.id != id, Nganh.ma_nganh == ma_nganh).first()
    if nganh:
        return jsonify({'duplicate': 'Mã ngành đã tồn tại. Không thể lưu ngành này.'})

    nganh = Nganh.query.filter(Nganh.id != id, Nganh.ten_nganh == ten_nganh).first()
    if nganh:
        return jsonify({'duplicate': 'Tên ngành đã tồn tại. Không thể lưu ngành này.'})

    nganh = Nganh(**request.form)
    found_nganh.ma_nganh = nganh.ma_nganh
    found_nganh.ten_nganh = nganh.ten_nganh
    found_nganh.khoa_id = nganh.khoa_id
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/nganh/<int:id>', methods=['DELETE'])
@login_required
def deleteNganh(id):
    nganh = Nganh.query.get_or_404(id)
    if nganh is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(nganh)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Bộ Môn------------------------------------------

@blueprint.route('/bomon')
@login_required
def bomon():
    create_bomon_form = CreateBoMonForm(request.form)
    khoa =  Khoa.query.all()
    create_bomon_form.khoa_id.choices = [(row.id, row.ten_khoa) for row in khoa]
    return render_template('home/bomon.html', segment='bomon', form=create_bomon_form)

@blueprint.route('/bomon', methods=['POST'])
@login_required
def addBoMon():
    ma_bomon = request.form['ma_bomon']
    ten_bomon = request.form['ten_bomon']

    bomon = BoMon.query.filter_by(ma_bomon=ma_bomon).first()
    if bomon:
        return jsonify({'duplicate': 'Mã bộ môn đã tồn tại. Không thể lưu bộ môn này.'})

    bomon = BoMon.query.filter_by(ten_bomon=ten_bomon).first()
    if bomon:
        return jsonify({'duplicate': 'Tên bộ môn đã tồn tại. Không thể lưu bộ môn này.'})

    bomon = BoMon(**request.form)
    db.session.add(bomon)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/bomon/<int:id>', methods=['PUT'])
@login_required
def updateBoMon(id):
    ma_bomon = request.form['ma_bomon']
    ten_bomon = request.form['ten_bomon']

    found_bomon = BoMon.query.filter_by(id=id).first()

    bomon = BoMon.query.filter(BoMon.id != id, BoMon.ma_bomon == ma_bomon).first()
    if bomon:
        return jsonify({'duplicate': 'Mã bộ môn đã tồn tại. Không thể lưu bộ môn này.'})

    bomon = BoMon.query.filter(BoMon.id != id, BoMon.ten_bomon == ten_bomon).first()
    if bomon:
        return jsonify({'duplicate': 'Tên bộ môn đã tồn tại. Không thể lưu bộ môn này.'})

    bomon = BoMon(**request.form)
    found_bomon.ma_bomon = bomon.ma_bomon
    found_bomon.ten_bomon = bomon.ten_bomon
    found_bomon.khoa_id = bomon.khoa_id
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/bomon/<int:id>', methods=['DELETE'])
@login_required
def deleteBoMon(id):
    bomon = BoMon.query.get_or_404(id)
    if bomon is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(bomon)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Môn học------------------------------------------

@blueprint.route('/mon')
@login_required
def mon():
    create_mon_form = CreateMonForm(request.form)
    khoa =  Khoa.query.all()
    create_mon_form.bomon_id.choices = dict([(row.ten_khoa, [(bomon.id, bomon.ten_bomon) for bomon in row.bomons]) for row in khoa])
    return render_template('home/mon.html', segment='mon', form=create_mon_form)

@blueprint.route('/mon', methods=['POST'])
@login_required
def addMon():
    ma_mon = request.form['ma_mon']
    ten_mon = request.form['ten_mon']

    mon = Mon.query.filter_by(ma_mon=ma_mon).first()
    if mon:
        return jsonify({'duplicate': 'Mã môn đã tồn tại. Không thể lưu môn này.'})

    mon = Mon.query.filter_by(ten_mon=ten_mon).first()
    if mon:
        return jsonify({'duplicate': 'Tên môn đã tồn tại. Không thể lưu môn này.'})

    mon = Mon(**request.form)
    db.session.add(mon)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/mon/<int:id>', methods=['PUT'])
@login_required
def updateMon(id):
    ma_mon = request.form['ma_mon']
    ten_mon = request.form['ten_mon']

    found_mon = Mon.query.filter_by(id=id).first()

    mon = Mon.query.filter(Mon.id != id, Mon.ma_mon == ma_mon).first()
    if mon:
        return jsonify({'duplicate': 'Mã môn đã tồn tại. Không thể lưu môn này.'})

    mon = Mon.query.filter(Mon.id != id, Mon.ten_mon == ten_mon).first()
    if mon:
        return jsonify({'duplicate': 'Tên môn đã tồn tại. Không thể lưu môn này.'})

    mon = Mon(**request.form)
    found_mon.ma_mon = mon.ma_mon
    found_mon.ten_mon = mon.ten_mon
    found_mon.bomon_id = mon.bomon_id
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/mon/<int:id>', methods=['DELETE'])
@login_required
def deleteMon(id):
    mon = Mon.query.get_or_404(id)
    if mon is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(mon)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Chương trình đào tạo------------------------------------------

@blueprint.route('/chuongtrinhdaotao')
@login_required
def chuongTrinhDaoTao():
    create_ctdt_form = CreateChuongTrinhDaoTaoForm(request.form)
    khoa = Khoa.query.all()
    create_ctdt_form.nganh_id.choices = dict([(row.ten_khoa, [(nganh.id, nganh.ten_nganh) for nganh in row.nganhs]) for row in khoa])
    bomon = BoMon.query.all()
    create_ctdt_form.mon_id.choices = dict([(row.ten_bomon, [(mon.id, mon.ten_mon) for mon in row.mons]) for row in bomon])
    return render_template('home/chuongtrinhdaotao.html', segment='chuongtrinhdaotao', form=create_ctdt_form)

@blueprint.route('/chuongtrinhdaotao', methods=['POST'])
@login_required
def addChuongTrinhDaoTao():
    ma_ctdt = request.form['ma_ctdt']
    ten_ctdt = request.form['ten_ctdt']
    mon_id = request.form.getlist('mon_id')

    ctdt = ChuongTrinhDaoTao.query.filter_by(ma_ctdt=ma_ctdt).first()
    if ctdt:
        return jsonify({'duplicate': 'Mã chương trình đào tạo đã tồn tại. Không thể lưu chương trình đào tạo này.'})

    ctdt = ChuongTrinhDaoTao.query.filter_by(ten_ctdt=ten_ctdt).first()
    if ctdt:
        return jsonify({'duplicate': 'Tên chương trình đào tạo đã tồn tại. Không thể lưu chương trình đào tạo này.'})

    ctdt = ChuongTrinhDaoTao(**request.form) 
    for row in mon_id:
        ctdt.mons.append(Mon.query.get(row))
        # db.session.add(ChuongTrinhDaoTao_MonHoc(ctdt_id = ma_ctdt, mon_id = mon_id))
    db.session.add(ctdt)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/chuongtrinhdaotao/<int:id>', methods=['PUT'])
@login_required
def updateChuongTrinhDaoTao(id):
    ma_ctdt = request.form['ma_ctdt']
    ten_ctdt = request.form['ten_ctdt']
    mon_id = request.form.getlist('mon_id')

    found_ctdt = ChuongTrinhDaoTao.query.filter_by(id=id).first()

    ctdt = ChuongTrinhDaoTao.query.filter(ChuongTrinhDaoTao.id != id, ChuongTrinhDaoTao.ma_ctdt == ma_ctdt).first()
    if ctdt:
        return jsonify({'duplicate': 'Mã chương trình đào tạo đã tồn tại. Không thể lưu chương trình đào tạo này.'})

    ctdt = ChuongTrinhDaoTao.query.filter(ChuongTrinhDaoTao.id != id, ChuongTrinhDaoTao.ten_ctdt == ten_ctdt).first()
    if ctdt:
        return jsonify({'duplicate': 'Tên chương trình đào tạo đã tồn tại. Không thể lưu chương trình đào tạo này.'})

    # ctdts = ChuongTrinhDaoTao.query.get(id)
    # print(ctdts.mons)

    ctdt = ChuongTrinhDaoTao(**request.form)
    found_ctdt.ma_ctdt = ctdt.ma_ctdt
    found_ctdt.ten_ctdt = ctdt.ten_ctdt
    found_ctdt.nganh_id = ctdt.nganh_id
    found_ctdt.mons = []

    for row in mon_id:
        found_ctdt.mons.append(Mon.query.get(row))
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/chuongtrinhdaotao/<int:id>', methods=['DELETE'])
@login_required
def deleteChuongTrinhDaoTao(id):
    ctdt = ChuongTrinhDaoTao.query.get_or_404(id)
    if ctdt is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(ctdt)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Giảng viên------------------------------------------

@blueprint.route('/giangvien')
@login_required
def giangVien():
    create_gv_form = CreateGiangVienForm(request.form)
    khoa =  Khoa.query.all()
    create_gv_form.bomon_id.choices = dict([(row.ten_khoa, [(bomon.id, bomon.ten_bomon) for bomon in row.bomons]) for row in khoa])
    return render_template('home/giangvien.html', segment='giangvien', form=create_gv_form)

@blueprint.route('/giangvien', methods=['POST'])
@login_required
def addGiangVien():
    ma_gv = request.form['ma_gv']
    email = request.form['email']
    phone = request.form['phone']

    gv = Person.query.filter_by(pcode=ma_gv).first()
    if gv:
        return jsonify({'duplicate': 'Mã giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = Person.query.filter_by(email=email).first()
    if gv:
        return jsonify({'duplicate': 'Email của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = Person.query.filter_by(phone=phone).first()
    if gv:
        return jsonify({'duplicate': 'Số điện thoại của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien(**request.form) 
    gv.pcode = ma_gv
    gv.username = gv.pcode
    db.session.add(gv)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/giangvien/<int:id>', methods=['PUT'])
@login_required
def updateGiangVien(id):
    ma_gv = request.form['ma_gv']
    email = request.form['email']
    phone = request.form['phone']

    found_gv = GiangVien.query.filter_by(id=id).first()

    gv = Person.query.filter(Person.id != id, Person.pcode == ma_gv).first()
    if gv:
        return jsonify({'duplicate': 'Mã giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = Person.query.filter(Person.id != id, Person.email == email).first()
    if gv:
        return jsonify({'duplicate': 'Email của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = Person.query.filter(Person.id != id, Person.phone == phone).first()
    if gv:
        return jsonify({'duplicate': 'Số điện thoại của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien(**request.form)
    found_gv.pcode = ma_gv
    found_gv.first_name = gv.first_name
    found_gv.last_name = gv.last_name
    found_gv.date_birth = gv.date_birth
    found_gv.address = gv.address
    found_gv.xa = gv.xa
    found_gv.quan = gv.quan
    found_gv.city = gv.city
    found_gv.email = gv.email
    found_gv.phone = gv.phone
    found_gv.bomon_id = gv.bomon_id
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/giangvien/<int:id>', methods=['DELETE'])
@login_required
def deleteGiangVien(id):
    gv = GiangVien.query.get_or_404(id)
    if gv is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(gv)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Lớp chuyên ngành------------------------------------------

@blueprint.route('/lopchuyennganh')
@login_required
def lopChuyenNganh():
    create_lcn_form = CreateLopChuyenNganhForm(request.form)
    bomon = BoMon.query.all()
    create_lcn_form.gv_id.choices = dict([(row.ten_bomon, [(gv.id, gv.pcode+' - '+gv.last_name+' '+gv.first_name) for gv in row.gvs]) for row in bomon])
    nganh = Nganh.query.all()
    create_lcn_form.ctdt_id.choices = dict([(row.ten_nganh, [(ctdt.id, ctdt.ten_ctdt) for ctdt in row.ctdts]) for row in nganh])
    sv = SinhVien.query.all()
    create_lcn_form.sv_id.choices = [(row.id, row.pcode+' - '+row.last_name+' '+row.first_name) for row in sv]
    return render_template('home/lopchuyennganh.html', segment='lopchuyennganh', form=create_lcn_form)

@blueprint.route('/lopchuyennganh', methods=['POST'])
@login_required
def addLopChuyenNganh():
    ten_lcn = request.form['ten_lcn']
    sv_id = request.form.getlist('sv_id')

    lcn = LopChuyenNganh.query.filter_by(ten_lcn=ten_lcn).first()
    if lcn:
        return jsonify({'duplicate': 'Tên lớp chuyên ngành đã tồn tại. Không thể lưu lớp chuyên ngành này.'})

    lcn = LopChuyenNganh(**request.form) 
    for row in sv_id:
        lcn.svs.append(SinhVien.query.get(row))
    db.session.add(lcn)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/lopchuyennganh/<int:id>', methods=['PUT'])
@login_required
def updateLopChuyenNganh(id):
    ten_lcn = request.form['ten_lcn']
    sv_id = request.form.getlist('sv_id')

    found_lcn = LopChuyenNganh.query.filter_by(id=id).first()

    lcn = LopChuyenNganh.query.filter(LopChuyenNganh.id != id, LopChuyenNganh.ten_lcn == ten_lcn).first()
    if lcn:
        return jsonify({'duplicate': 'Tên lớp chuyên ngành đã tồn tại. Không thể lưu lớp chuyên ngành này.'})


    lcn = LopChuyenNganh(**request.form)
    found_lcn.ten_lcn = lcn.ten_lcn
    found_lcn.ctdt_id = lcn.ctdt_id
    found_lcn.gv_id = lcn.gv_id
    found_lcn.svs = []

    for row in sv_id:
        found_lcn.svs.append(SinhVien.query.get(row))
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/lopchuyennganh/<int:id>', methods=['DELETE'])
@login_required
def deleteLopChuyenNganh(id):
    lcn = LopChuyenNganh.query.get_or_404(id)
    if lcn is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(lcn)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Sinh viên------------------------------------------

@blueprint.route('/sinhvien')
@login_required
def sinhVien():
    create_sv_form = CreateSinhVienForm(request.form)
    ctdt = ChuongTrinhDaoTao.query.all()
    create_sv_form.lcn_id.choices = dict([(row.ten_ctdt, [(lcn.id, lcn.ten_lcn) for lcn in row.lcns]) for row in ctdt])

    create_filter_nam_form = CreateFilterNamHocForm(request.form)
    nam = Nam.query.all()
    create_filter_nam_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]

    return render_template('home/sinhvien.html', segment='sinhvien', form=create_sv_form, formNam = create_filter_nam_form)

@blueprint.route('/sinhvien', methods=['POST'])
@login_required
def addSinhVien():
    ma_sv = request.form['ma_sv']
    email = request.form['email']
    phone = request.form['phone']
    lcn_id = request.form.getlist('lcn_id')

    sv = Person.query.filter_by(pcode=ma_sv).first()
    if sv:
        return jsonify({'duplicate': 'Mã sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = Person.query.filter_by(email=email).first()
    if sv:
        return jsonify({'duplicate': 'Email của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = Person.query.filter_by(phone=phone).first()
    if sv:
        return jsonify({'duplicate': 'Số điện thoại của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien(**request.form)
    sv.pcode = ma_sv
    sv.username = sv.pcode
    for row in lcn_id:
        sv.lcns.append(LopChuyenNganh.query.get(row))
    db.session.add(sv)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/sinhvien/<int:id>', methods=['PUT'])
@login_required
def updateSinhVien(id):
    ma_sv = request.form['ma_sv']
    email = request.form['email']
    phone = request.form['phone']
    lcn_id = request.form.getlist('lcn_id')

    found_sv = SinhVien.query.filter_by(id=id).first()

    sv = Person.query.filter(Person.id != id, Person.pcode == ma_sv).first()
    if sv:
        return jsonify({'duplicate': 'Mã sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = Person.query.filter(Person.id != id, Person.email == email).first()
    if sv:
        return jsonify({'duplicate': 'Email của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = Person.query.filter(Person.id != id, Person.phone == phone).first()
    if sv:
        return jsonify({'duplicate': 'Số điện thoại của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien(**request.form)
    found_sv.pcode = ma_sv
    found_sv.first_name = sv.first_name
    found_sv.last_name = sv.last_name
    found_sv.date_birth = sv.date_birth
    found_sv.address = sv.address
    found_sv.xa = sv.xa
    found_sv.quan = sv.quan
    found_sv.city = sv.city
    found_sv.email = sv.email
    found_sv.phone = sv.phone
    found_sv.lcns = []

    for row in lcn_id:
        found_sv.lcns.append(LopChuyenNganh.query.get(row))
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/sinhvien/<int:id>', methods=['DELETE'])
@login_required
def deleteSinhVien(id):
    sv = SinhVien.query.get_or_404(id)
    if sv is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(sv)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Lớp Học------------------------------------------

@blueprint.route('/lop')
@login_required
def lop():
    create_lop_form = CreateLopForm(request.form)
    nam = Nam.query.all()
    create_lop_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]

    bomon = BoMon.query.all()
    create_lop_form.mon_id.choices = dict([(row.ten_bomon, [(mon.id, mon.ma_mon + ' - ' + mon.ten_mon) for mon in row.mons]) for row in bomon])

    create_lichlop_form = CreateLichLopForm(request.form)
    mon = Mon.query.all()
    create_lichlop_form.lop_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])
    bomon = BoMon.query.all()
    create_lichlop_form.gv_id.choices = dict([(row.ten_bomon, [(gv.id, gv.pcode+' - '+gv.last_name+' '+gv.first_name) for gv in row.gvs]) for row in bomon])
    create_lichlop_form.phong_id.choices = [(row.id, row.ten_phong) for row in Phong.query.all()]

    create_sv_lop_form = CreateSinhVien_LopForm(request.form)
    create_sv_lop_form.lop_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])
    sv = SinhVien.query.all()
    create_sv_lop_form.sv_id.choices = [(row.id, row.pcode+' - '+row.last_name+' '+row.first_name) for row in sv]
    
    return render_template('home/lop.html', segment='lop', forml=create_lop_form, formll=create_lichlop_form, formsv=create_sv_lop_form)

@blueprint.route('/lop', methods=['POST'])
@login_required
def addLop():
    ten_lop = request.form['ten_lop']
    ky_id = request.form['ky_id']

    lop = Lop.query.filter(Lop.ky_id == ky_id, Lop.ten_lop == ten_lop).first()
    if lop:
        return jsonify({'duplicate': 'Lớp học đã tồn tại. Không thể lưu lớp học này.'})


    lop = Lop(**request.form)
    # for row in lcn_id:
    #     lop.lcns.append(LopChuyenNganh.query.get(row))
    db.session.add(lop)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/lop/<int:id>', methods=['PUT'])
@login_required
def updateLop(id):
    ten_lop = request.form['ten_lop']
    mon_id = int(request.form['mon_id'])
    ky_id = request.form['ky_id']
    # lcn_id = request.form.getlist('lcn_id')

    found_lop = Lop.query.filter_by(id=id).first()

    lop = Lop.query.filter(Lop.id != id, Lop.ky_id == ky_id, Lop.ten_lop == ten_lop).first()
    if lop:
        return jsonify({'duplicate': 'Lớp học đã tồn tại. Không thể lưu lớp học này.'})

    svs = SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == id).all()
    for sv in svs:
        lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv.sv_id, SinhVien_Lop.lop_id != id).all()
        for lop in lops:
            check = Lop.query.filter(Lop.ky_id == ky_id, Lop.id == lop.lop_id).first()
            if check:
                mon = Lop.query.filter(Lop.id == lop.lop_id).first()
                if mon.mon_id == mon_id:
                    return jsonify({'duplicate': 'Lớp học này tồn tại sinh viên đã đăng ký học phần này. Không thể lưu lớp học này.'})


    lop = Lop(**request.form)
    found_lop.ten_lop = lop.ten_lop
    found_lop.so_luong = lop.so_luong
    found_lop.mon_id = lop.mon_id
    found_lop.ky_id = lop.ky_id
    # found_lop.lcns = []

    # for row in lcn_id:
    #     found_lop.lcns.append(LopChuyenNganh.query.get(row))
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/lop/<int:id>', methods=['DELETE'])
@login_required
def deleteLop(id):
    lop = Lop.query.get_or_404(id)
    if lop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(lop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Phòng Học------------------------------------------

@blueprint.route('/phong')
@login_required
def phong():
    create_phong_form = CreatePhongForm(request.form)
    return render_template('home/phong.html', segment='phong', form=create_phong_form)

@blueprint.route('/phong', methods=['POST'])
def addPhong():
    ten_phong = request.form['ten_phong']

    phong = Phong.query.filter_by(ten_phong=ten_phong).first()
    if phong:
        return jsonify({'duplicate': 'Phòng đã tồn tại. Không thể lưu phòng này.'})

    phong = Phong(**request.form)
    db.session.add(phong)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/phong/<int:id>', methods=['PUT'])
@login_required
def updatePhong(id):
    ten_phong = request.form['ten_phong']

    found_phong = Phong.query.filter_by(id=id).first()

    phong = Phong.query.filter(Phong.id != id, Phong.ten_phong == ten_phong).first()
    if phong:
        return jsonify({'duplicate': 'Phòng đã tồn tại. Không thể lưu phòng này.'})

    phong = Phong(**request.form)
    found_phong.ten_phong = phong.ten_phong
    found_phong.so_luong = phong.so_luong
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/phong/<int:id>', methods=['DELETE'])
@login_required
def deletePhong(id):
    phong = Phong.query.get_or_404(id)
    if phong is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(phong)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Lịch Lớp------------------------------------------

@blueprint.route('/lichlop')
@login_required
def lichlop():
    create_lichlop_form = CreateLichLopForm(request.form)
    mon = Mon.query.all()
    create_lichlop_form.lop_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])
    bomon = BoMon.query.all()
    create_lichlop_form.gv_id.choices = dict([(row.ten_bomon, [(gv.id, gv.pcode+' - '+gv.last_name+' '+gv.first_name) for gv in row.gvs]) for row in bomon])
    create_lichlop_form.phong_id.choices = [(row.id, row.ten_phong) for row in Phong.query.all()]
    return render_template('home/lichlop.html', segment='lichlop', form=create_lichlop_form)

@blueprint.route('/lichlop', methods=['POST'])
@login_required
def addLichLop():
    lop_id = int(request.form['lop_id'])
    thu = int(request.form['thu'])
    start = int(request.form['start'])
    end = int(request.form['end'])
    gv_id = request.form['gv_id']
    phong_id = request.form['phong_id']
    ky_id = request.form['ky_id']
    # lcn_id = request.form.getlist('lcn_id')

    lichlop = LichLop.query.filter(LichLop.thu == thu, LichLop.lop_id == lop_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
    if lichlop:
        return jsonify({'duplicate': 'Lịch lớp học bị trùng ca. Không thể lưu lịch lớp học này.'})

    lops = Lop.query.filter(Lop.ky_id == ky_id).all()
    for lop in lops:
        lichlop = LichLop.query.filter(LichLop.lop_id == lop.id, LichLop.thu == thu, LichLop.phong_id == phong_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
        if lichlop:
            return jsonify({'duplicate': 'Lịch lớp học bị trùng phòng. Không thể lưu lịch lớp học này.'})

    if gv_id != '':
        lops = Lop.query.filter(Lop.ky_id == ky_id).all()
        for lop in lops:
            lichlop = LichLop.query.filter(LichLop.lop_id == lop.id, LichLop.thu == thu, LichLop.gv_id == gv_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
            if lichlop:
                return jsonify({'duplicate': 'Giảng viên giảng dạy lớp này bị trùng lịch. Không thể lưu lịch lớp học này.'})

    svs = SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == lop_id).all()
    for sv in svs:
        lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv.sv_id, SinhVien_Lop.lop_id != lop_id).all()
        for lop in lops: 
            check = Lop.query.filter(Lop.ky_id == ky_id, Lop.id == lop.lop_id).first()
            if check:
                lichlop2 = LichLop.query.filter(LichLop.lop_id == lop.lop_id).all()
                for row2 in lichlop2:
                    if row2.thu == thu:
                        if((row2.start<=start and start<=row2.end) or (row2.start<=end and end<=row2.end)):
                            return jsonify({'duplicate': 'Lịch lớp này có sinh viên này bị trùng. Không thể thêm lịch lớp này.'})


    lichlop = LichLop(**request.form)
    # for row in lcn_id:
    #     lichlop.lcns.append(LichLopChuyenNganh.query.get(row))
    db.session.add(lichlop)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/lichlop/<int:id>', methods=['PUT'])
@login_required
def updateLichLop(id):
    lop_id = int(request.form['lop_id'])
    thu = int(request.form['thu'])
    start = int(request.form['start'])
    end = int(request.form['end'])
    gv_id = request.form['gv_id']
    phong_id = request.form['phong_id']
    ky_id = request.form['ky_id']

    found_lichlop = LichLop.query.filter_by(id=id).first()

    lichlop = LichLop.query.filter(LichLop.id != id, LichLop.thu == thu, LichLop.lop_id == lop_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
    if lichlop:
        return jsonify({'duplicate': 'Lịch lớp học bị trùng ca. Không thể lưu lịch lớp học này.'})

    lops = Lop.query.filter(Lop.ky_id == ky_id).all()
    for lop in lops:
        lichlop = LichLop.query.filter(LichLop.lop_id == lop.id, LichLop.id != id, LichLop.thu == thu, LichLop.phong_id == phong_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
        if lichlop:
            return jsonify({'duplicate': 'Lịch lớp học bị trùng phòng. Không thể lưu lịch lớp học này.'})

    if gv_id != '':
        lops = Lop.query.filter(Lop.ky_id == ky_id).all()
        for lop in lops:
            lichlop = LichLop.query.filter(LichLop.lop_id == lop.id, LichLop.id != id, LichLop.thu == thu, LichLop.gv_id == gv_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
            if lichlop:
                return jsonify({'duplicate': 'Giảng viên giảng dạy lớp này bị trùng lịch. Không thể lưu lịch lớp học này.'})

    svs = SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == lop_id).all()
    for sv in svs:
        lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv.sv_id, SinhVien_Lop.lop_id != lop_id).all()
        for lop in lops: 
            check = Lop.query.filter(Lop.ky_id == ky_id, Lop.id == lop.lop_id).first()
            if check:
                lichlop2 = LichLop.query.filter(LichLop.lop_id == lop.lop_id).all()
                for row2 in lichlop2:
                    if row2.thu == thu:
                        if((row2.start<=start and start<=row2.end) or (row2.start<=end and end<=row2.end)):
                            return jsonify({'duplicate': 'Lịch lớp này có sinh viên này bị trùng. Không thể thêm lịch lớp này.'})


    lichlop = LichLop(**request.form)
    found_lichlop.lop_id = lichlop.lop_id
    found_lichlop.thu = lichlop.thu
    found_lichlop.start = lichlop.start
    found_lichlop.end = lichlop.end
    found_lichlop.gv_id = lichlop.gv_id
    found_lichlop.phong_id = lichlop.phong_id
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/lichlop/<int:id>', methods=['DELETE'])
@login_required
def deleteLichLop(id):
    lichlop = LichLop.query.get_or_404(id)
    if lichlop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(lichlop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Sinh Viên - Lớp------------------------------------------

@blueprint.route('/sv_lop', methods=['POST'])
@login_required
def addSVLop():
    lop_id = int(request.form['lop_id'])
    sv_id = int(request.form['sv_id'])
    ky_id = int(request.form['ky_id'])

    lichlop1 = LichLop.query.filter(LichLop.lop_id == lop_id).all()
    mon1 = Lop.query.filter(Lop.id == lop_id).first()

    lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id).all()

    for lop in lops:
        mon2 = Lop.query.filter(Lop.mon_id == lop.lop.mon_id).first()
        if mon2 is not None and mon1.mon_id == mon2.mon_id:
            return jsonify({'duplicate': 'Sinh viên này đã đăng ký học phần này. Không thể thêm sinh viên này.'})

    for lop in lops:
        check = Lop.query.filter(Lop.ky_id == ky_id, Lop.id == lop.lop_id).first()
        if check:
            lichlop2 = LichLop.query.filter(LichLop.lop_id == lop.lop_id).all()
            for row2 in lichlop2:
                for row1 in lichlop1:
                    if row2.thu == row1.thu:
                        if((row2.start<=row1.start and row1.start<=row2.end) or (row2.start<=row1.end and row1.end<=row2.end)):
                            return jsonify({'duplicate': 'Sinh viên này bị trùng lịch. Không thể thêm sinh viên này.'})


    sv_lop = SinhVien_Lop(**request.form)
    # for row in lcn_id:
    #     sv_lop.lcns.append(SinhVien_LopChuyenNganh.query.get(row))
    db.session.add(sv_lop)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})


@blueprint.route('/sv_lop/<int:id>', methods=['DELETE'])
@login_required
def deleteSVLop(id):
    sv_lop = SinhVien_Lop.query.get_or_404(id)
    if sv_lop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(sv_lop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Năm Học------------------------------------------

@blueprint.route('/nam')
@login_required
def nam():
    create_nam_form = CreateNamForm(request.form)
    create_ky_form = CreateKyForm(request.form)
    return render_template('home/nam.html', segment='nam', formn=create_nam_form, formk=create_ky_form)

@blueprint.route('/nam', methods=['POST'])
@login_required
def addNam():
    # namhoc = request.form['namhoc']
    hk1 = request.form['hk1']
    hk2 = request.form['hk2']
    hk3 = request.form['hk3']
    date_end = request.form['date_end']

    hk1s = Ky.query.filter(Ky.ten_ky == 1).all()
    for ky in hk1s:
        if ky.date_start.year == (datetime.strptime(hk1, '%Y-%m-%d')).year:
            return jsonify({'duplicate': 'Năm học đã tồn tại. Không thể lưu năm học này.'})

    # nam = Nam.query.filter(or_(Nam.start == start, Nam.end == end)).first()
    # if nam:
    #     return jsonify({'duplicate': 'Năm học đã tồn tại. Không thể lưu năm học này.'})

    nam = Nam(**request.form)
    db.session.add(nam)
    db.session.commit()

    id = (Nam.query.filter(Nam.date_end == nam.date_end).first()).id

    ky1 = Ky(ten_ky = 1, date_start = hk1, nam_id = id)
    ky2 = Ky(ten_ky = 2, date_start = hk2, nam_id = id)
    ky3 = Ky(ten_ky = 3, date_start = hk3, nam_id = id)

    db.session.add(ky1)
    db.session.add(ky2)
    db.session.add(ky3)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/nam/<int:id>', methods=['PUT'])
@login_required
def updateNam(id):
    hk1 = request.form['hk1']
    hk2 = request.form['hk2']
    hk3 = request.form['hk3']
    date_end = request.form['date_end']

    found_nam = Nam.query.filter_by(id=id).first()


    hk1s = Ky.query.filter(Ky.nam_id != id, Ky.ten_ky == 1).all()
    for ky in hk1s:
        if ky.date_start.year == (datetime.strptime(hk1, '%Y-%m-%d')).year:
            return jsonify({'duplicate': 'Năm học đã tồn tại. Không thể lưu năm học này.'})

    # nam = Nam.query.filter(Nam.id != id, or_(Nam.start == start, Nam.end == end)).first()
    # if nam:
    #     return jsonify({'duplicate': 'Năm học đã tồn tại. Không thể lưu năm học này.'})

    nam = Nam(**request.form)
    found_nam.date_end = nam.date_end
    for ky in found_nam.kys:
        if ky.ten_ky == 1:
            ky.date_start = datetime.strptime(hk1, '%Y-%m-%d')
        elif ky.ten_ky == 2:
            ky.date_start = datetime.strptime(hk2, '%Y-%m-%d')
        elif ky.ten_ky == 3:
            ky.date_start = datetime.strptime(hk3, '%Y-%m-%d')
    db.session.commit()
  
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/nam/<int:id>', methods=['DELETE'])
@login_required
def deleteNam(id):
    nam = Nam.query.get_or_404(id)
    if nam is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(nam)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Kỳ Học------------------------------------------

@blueprint.route('/ky/<int:id>', methods=['PUT'])
@login_required
def updateKy(id):

    found_ky = Ky.query.filter_by(id=id).first()

    ky = Ky(**request.form)
    found_ky.dkh_start = ky.dkh_start
    found_ky.dkh_end = ky.dkh_end
    found_ky.dkt_start = ky.dkt_start
    found_ky.dkt_end = ky.dkt_end
    db.session.commit()
  
    return jsonify({'success': 'Cập nhật thành công.'})



#-------------------------------------Lịch Thi------------------------------------------

@blueprint.route('/lichthi')
@login_required
def lichthi():
    create_lichthi_form = CreateLichThiForm(request.form)
    nam = Nam.query.all()
    create_lichthi_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]

    bomon = BoMon.query.all()
    create_lichthi_form.mon_id.choices = dict([(row.ma_bomon + ' - ' + row.ten_bomon, [(mon.id, mon.ma_mon + ' - ' + mon.ten_mon) for mon in row.mons]) for row in bomon])

    create_lichthi_form.phong_id.choices = [(row.id, row.ten_phong) for row in Phong.query.all()]


    create_sv_lichthi_form = CreateSinhVien_LichThiForm(request.form)

    return render_template('home/lichthi.html', segment='lichthi', form=create_lichthi_form, formsv=create_sv_lichthi_form)

@blueprint.route('/lichthi', methods=['POST'])
@login_required
def addLichThi():
    mon_id = request.form['mon_id']
    date = request.form['date']
    start = request.form['start']
    end = request.form['end']
    phong_id = request.form['phong_id']
    ky_id = request.form['ky_id']
    # lcn_id = request.form.getlist('lcn_id')

    lop = Lop.query.filter(Lop.ky_id == ky_id, Lop.mon_id == mon_id).first()
    if not lop:
        return jsonify({'duplicate': 'Kỳ này không có môn học này. Không thể lưu lịch thi này.'})

    lichthi = LichThi.query.filter(LichThi.date == date, LichThi.phong_id == phong_id, or_(and_(LichThi.start <= start, start <= LichThi.end), and_(LichThi.start <= end, end <= LichThi.end))).first()
    if lichthi:
        return jsonify({'duplicate': 'Lịch thi bị trùng. Không thể lưu lịch thi này.'})


    lichthi = LichThi(**request.form)
    # for row in lcn_id:
    #     lichthi.lcns.append(LichThiChuyenNganh.query.get(row))
    db.session.add(lichthi)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/lichthi/<int:id>', methods=['PUT'])
@login_required
def updateLichThi(id):
    mon_id = request.form['mon_id']
    date = request.form['date']
    start = request.form['start']
    end = request.form['end']
    phong_id = request.form['phong_id']
    ky_id = request.form['ky_id']

    found_lichthi = LichThi.query.filter_by(id=id).first()

    lop = Lop.query.filter(Lop.ky_id == ky_id, Lop.mon_id == mon_id).first()
    if not lop:
        return jsonify({'duplicate': 'Kỳ này không có môn học này. Không thể lưu lịch thi này.'})

    lichthi = LichThi.query.filter(LichThi.id != id, LichThi.date == date, LichThi.phong_id == phong_id, or_(and_(LichThi.start <= start, start <= LichThi.end), and_(LichThi.start <= end, end <= LichThi.end))).first()
    if lichthi:
        return jsonify({'duplicate': 'Lịch thi bị trùng. Không thể lưu lịch thi này.'})


    lichthi = LichThi(**request.form)
    found_lichthi.mon_id = lichthi.mon_id
    found_lichthi.date = lichthi.date
    found_lichthi.start = lichthi.start
    found_lichthi.end = lichthi.end
    found_lichthi.ky_id = lichthi.ky_id
    found_lichthi.phong_id = lichthi.phong_id
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/lichthi/<int:id>', methods=['DELETE'])
@login_required
def deleteLichThi(id):
    lichthi = LichThi.query.get_or_404(id)
    if lichthi is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(lichthi)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})




#-------------------------------------Sinh viên - Lịch thi------------------------------------------

@blueprint.route('/sv_lichthi/<int:lichthi_id>', methods=['PUT'])
@login_required
def updateSV_LichThi(lichthi_id):
    sv_id = request.form.getlist('sv_id')

    found_lichthi = LichThi.query.filter_by(id=lichthi_id).first()


    # lcn = LichThi(**request.form)
    found_lichthi.sv_lichthis = []

    for row in sv_id:
        sv_thi = SinhVien_LichThi(lichthi_id = lichthi_id, sv_id = row)
        db.session.add(sv_thi)
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})



#-------------------------------------Bảng điểm------------------------------------------

@blueprint.route('/bangdiem')
@login_required
def bangDiem():
    create_bangdiem_form = CreateBangDiemForm(request.form)
    nam = Nam.query.all()
    create_bangdiem_form.nam_id.choices = [(row.id, 'Năm học ' + str((Ky.query.filter(Ky.nam_id == row.id, Ky.ten_ky == 1).first()).date_start.year) + ' - ' + str(row.date_end.year)) for row in nam]

    # mon = Mon.query.all()
    # create_bangdiem_form.lop_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])
    # create_bangdiem_form.lichthi_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lichthi.id, lichthi.phong.ten_phong + ' ' + str(lichthi.start) + '-' + str(lichthi.end) + ' ' + lichthi.date.strftime("%Y-%m-%d")) for lichthi in row.lichthis]) for row in mon])


    return render_template('home/bangdiem.html', segment='bangdiem', form=create_bangdiem_form)

@blueprint.route('/bangdiem/<int:id>', methods=['PUT'])
@login_required
def updateBangDiem(id):
    if 'diemQT' in request.form:
        diemQT = request.form['diemQT']
        if diemQT == '':
            diemQT = None

        found_sv_lop = SinhVien_Lop.query.filter_by(id=id).first()

        # lcn = LichThi(**request.form)
        found_sv_lop.diemQT = diemQT
        db.session.commit()
        return jsonify({'success': 'Cập nhật thành công.'})
    elif 'diemCK' in request.form:
        diemCK = request.form['diemCK']
        if diemCK == '':
            diemCK = None

        found_sv_lichthi = SinhVien_LichThi.query.filter_by(id=id).first()

        # lcn = LichThi(**request.form)
        found_sv_lichthi.diemCK = diemCK
        db.session.commit()
        return jsonify({'success': 'Cập nhật thành công.'})
        
    return jsonify({'error': 'Cập nhật không thành công.'})



#-------------------------------------Kỳ Học------------------------------------------

# @blueprint.route('/ky')
# def ky():
#     create_ky_form = CreateKyForm(request.form)
#     return render_template('home/ky.html', segment='ky', form=create_ky_form)

# @blueprint.route('/ky', methods=['POST'])
# def addKy():
#     nam_id = request.form['nam_id']
#     ten_ky = request.form['ten_ky']

#     ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ten_ky).first()
#     if ky:
#         return jsonify({'duplicate': 'Kỳ học đã tồn tại. Không thể lưu kỳ học này.'})

#     ky = Ky(**request.form)
#     db.session.add(ky)
#     db.session.commit()
        
#     return jsonify({'success': 'Thêm thành công.'})

# @blueprint.route('/ky/<int:id>', methods=['PUT'])
# def updateKy(id):
#     nam_id = request.form['nam_id']
#     ten_ky = request.form['ten_ky']

#     found_ky = Ky.query.filter_by(id=id).first()

#     ky = Ky.query.filter(Ky.id != id, Ky.nam_id == nam_id, Ky.ten_ky == ten_ky).first()
#     if ky:
#         return jsonify({'duplicate': 'Năm học đã tồn tại. Không thể lưu năm học này.'})

#     ky = Ky(**request.form)
#     found_ky.nam_id = ky.nam_id
#     found_ky.ten_ky = ky.ten_ky
#     db.session.commit()
        
#     return jsonify({'success': 'Cập nhật thành công.'})

# @blueprint.route('/ky/<int:id>', methods=['DELETE'])
# def deleteKy(id):
#     ky = Ky.query.get_or_404(id)
#     if ky is None:
#         return jsonify({'error': 'Không tìm thấy.'})
#     db.session.delete(ky)
#     db.session.commit()
#     return jsonify({'success': 'Xóa thành công.'})





# @blueprint.route('/winemageda')
# def winemageda():
#     df = pd.read_csv("D:/Documents/LTPython/A35225/winemag-data-130k-v2.csv")
#     ndf = df.dropna()
#     top10 = ndf.sort_values(by='price', ascending=False).iloc[0:10]

#     county = df.groupby('country')['Unnamed: 0'].count()
#     #county = df.pivot_table(index='country', values=['Unnamed: 0'], aggfunc='count')
#     data = pd.DataFrame(county)
#     data.columns = ['count']
#     data = data.sort_values(by='count', ascending=False)

#     point = ndf.groupby('points')['Unnamed: 0'].count()
#     point = pd.DataFrame(point)
#     point.columns = ['count']

#     price = ndf.groupby('price')['Unnamed: 0'].count()
#     price = pd.DataFrame(price)
#     price.columns = ['count']
#     return render_template('home/winemageda.html', segment='winemageda', df=df.iterrows(), top10=top10.iterrows(), data=data.iterrows(), point=point.iterrows(), price=price.iterrows())

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None