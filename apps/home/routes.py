# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from re import S
from apps.authentication.forms import CreateKhoaForm, CreateNganhForm, CreateBoMonForm, CreateMonForm, CreateChuongTrinhDaoTaoForm, CreateLopChuyenNganhForm, CreateSinhVienForm, CreateGiangVienForm, CreateLopForm, CreatePhongForm, CreateLichLopForm, CreateSinhVien_LopForm, CreateNamForm, CreateKyForm
from apps.authentication.models import Khoa, Nganh, BoMon, Mon, ChuongTrinhDaoTao, GiangVien, LopChuyenNganh, SinhVien, Lop, Phong, LichLop, SinhVien_Lop, Nam, Ky, Users
from apps.home import blueprint
from apps import db, login_manager, create_app
from flask import Flask, render_template, jsonify, redirect, request, session, url_for, Response
from flask_login import login_required
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


#-------------------------------------Khoa------------------------------------------

@blueprint.route('/khoa')
def khoa():
    create_khoa_form = CreateKhoaForm(request.form)
    return render_template('home/khoa.html', segment='khoa', form=create_khoa_form)

@blueprint.route('/khoa', methods=['POST'])
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
def deleteKhoa(id):
    khoa = Khoa.query.get_or_404(id)
    if khoa is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(khoa)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Ngành------------------------------------------

@blueprint.route('/nganh')
def nganh():
    create_nganh_form = CreateNganhForm(request.form)
    khoa =  Khoa.query.all()
    create_nganh_form.khoa_id.choices = [(row.id, row.ten_khoa) for row in khoa]
    return render_template('home/nganh.html', segment='nganh', form=create_nganh_form)

@blueprint.route('/nganh', methods=['POST'])
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
def deleteNganh(id):
    nganh = Nganh.query.get_or_404(id)
    if nganh is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(nganh)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Bộ Môn------------------------------------------

@blueprint.route('/bomon')
def bomon():
    create_bomon_form = CreateBoMonForm(request.form)
    khoa =  Khoa.query.all()
    create_bomon_form.khoa_id.choices = [(row.id, row.ten_khoa) for row in khoa]
    return render_template('home/bomon.html', segment='bomon', form=create_bomon_form)

@blueprint.route('/bomon', methods=['POST'])
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
def deleteBoMon(id):
    bomon = BoMon.query.get_or_404(id)
    if bomon is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(bomon)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Môn học------------------------------------------

@blueprint.route('/mon')
def mon():
    create_mon_form = CreateMonForm(request.form)
    khoa =  Khoa.query.all()
    create_mon_form.bomon_id.choices = dict([(row.ten_khoa, [(bomon.id, bomon.ten_bomon) for bomon in row.bomons]) for row in khoa])
    return render_template('home/mon.html', segment='mon', form=create_mon_form)

@blueprint.route('/mon', methods=['POST'])
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
def deleteMon(id):
    mon = Mon.query.get_or_404(id)
    if mon is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(mon)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Chương trình đào tạo------------------------------------------

@blueprint.route('/chuongtrinhdaotao')
def chuongTrinhDaoTao():
    create_ctdt_form = CreateChuongTrinhDaoTaoForm(request.form)
    khoa = Khoa.query.all()
    create_ctdt_form.nganh_id.choices = dict([(row.ten_khoa, [(nganh.id, nganh.ten_nganh) for nganh in row.nganhs]) for row in khoa])
    bomon = BoMon.query.all()
    create_ctdt_form.mon_id.choices = dict([(row.ten_bomon, [(mon.id, mon.ten_mon) for mon in row.mons]) for row in bomon])
    return render_template('home/chuongtrinhdaotao.html', segment='chuongtrinhdaotao', form=create_ctdt_form)

@blueprint.route('/chuongtrinhdaotao', methods=['POST'])
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
def deleteChuongTrinhDaoTao(id):
    ctdt = ChuongTrinhDaoTao.query.get_or_404(id)
    if ctdt is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(ctdt)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Giảng viên------------------------------------------

@blueprint.route('/giangvien')
def giangVien():
    create_gv_form = CreateGiangVienForm(request.form)
    khoa =  Khoa.query.all()
    create_gv_form.bomon_id.choices = dict([(row.ten_khoa, [(bomon.id, bomon.ten_bomon) for bomon in row.bomons]) for row in khoa])
    return render_template('home/giangvien.html', segment='giangvien', form=create_gv_form)

@blueprint.route('/giangvien', methods=['POST'])
def addGiangVien():
    ma_gv = request.form['ma_gv']
    email = request.form['email']
    phone = request.form['phone']

    gv = GiangVien.query.filter_by(ma_gv=ma_gv).first()
    if gv:
        return jsonify({'duplicate': 'Mã giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien.query.filter_by(email=email).first()
    if gv:
        return jsonify({'duplicate': 'Email của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien.query.filter_by(phone=phone).first()
    if gv:
        return jsonify({'duplicate': 'Số điện thoại của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien(**request.form) 
    db.session.add(gv)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/giangvien/<int:id>', methods=['PUT'])
def updateGiangVien(id):
    ma_gv = request.form['ma_gv']
    email = request.form['email']
    phone = request.form['phone']

    found_gv = GiangVien.query.filter_by(id=id).first()

    gv = GiangVien.query.filter(GiangVien.id != id, GiangVien.ma_gv == ma_gv).first()
    if gv:
        return jsonify({'duplicate': 'Mã giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien.query.filter(GiangVien.id != id, GiangVien.email == email).first()
    if gv:
        return jsonify({'duplicate': 'Email của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien.query.filter(GiangVien.id != id, GiangVien.phone == phone).first()
    if gv:
        return jsonify({'duplicate': 'Số điện thoại của giảng viên đã tồn tại. Không thể lưu giảng viên này.'})

    gv = GiangVien(**request.form)
    found_gv.ma_gv = gv.ma_gv
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
def deleteGiangVien(id):
    gv = GiangVien.query.get_or_404(id)
    if gv is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(gv)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Lớp chuyên ngành------------------------------------------

@blueprint.route('/lopchuyennganh')
def lopChuyenNganh():
    create_lcn_form = CreateLopChuyenNganhForm(request.form)
    bomon = BoMon.query.all()
    create_lcn_form.gv_id.choices = dict([(row.ten_bomon, [(gv.id, gv.ma_gv+' - '+gv.last_name+' '+gv.first_name) for gv in row.gvs]) for row in bomon])
    nganh = Nganh.query.all()
    create_lcn_form.ctdt_id.choices = dict([(row.ten_nganh, [(ctdt.id, ctdt.ten_ctdt) for ctdt in row.ctdts]) for row in nganh])
    sv = SinhVien.query.all()
    create_lcn_form.sv_id.choices = [(row.id, row.ma_sv+' - '+row.last_name+' '+row.first_name) for row in sv]
    return render_template('home/lopchuyennganh.html', segment='lopchuyennganh', form=create_lcn_form)

@blueprint.route('/lopchuyennganh', methods=['POST'])
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
def deleteLopChuyenNganh(id):
    lcn = LopChuyenNganh.query.get_or_404(id)
    if lcn is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(lcn)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Sinh viên------------------------------------------

@blueprint.route('/sinhvien')
def sinhVien():
    create_sv_form = CreateSinhVienForm(request.form)
    ctdt = ChuongTrinhDaoTao.query.all()
    create_sv_form.lcn_id.choices = dict([(row.ten_ctdt, [(lcn.id, lcn.ten_lcn) for lcn in row.lcns]) for row in ctdt])
    return render_template('home/sinhvien.html', segment='sinhvien', form=create_sv_form)

@blueprint.route('/sinhvien', methods=['POST'])
def addSinhVien():
    ma_sv = request.form['ma_sv']
    email = request.form['email']
    phone = request.form['phone']
    lcn_id = request.form.getlist('lcn_id')

    sv = SinhVien.query.filter_by(ma_sv=ma_sv).first()
    if sv:
        return jsonify({'duplicate': 'Mã sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien.query.filter_by(email=email).first()
    if sv:
        return jsonify({'duplicate': 'Email của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien.query.filter_by(phone=phone).first()
    if sv:
        return jsonify({'duplicate': 'Số điện thoại của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien(**request.form)
    for row in lcn_id:
        sv.lcns.append(LopChuyenNganh.query.get(row))
    db.session.add(sv)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/sinhvien/<int:id>', methods=['PUT'])
def updateSinhVien(id):
    ma_sv = request.form['ma_sv']
    email = request.form['email']
    phone = request.form['phone']
    lcn_id = request.form.getlist('lcn_id')

    found_sv = SinhVien.query.filter_by(id=id).first()

    sv = SinhVien.query.filter(SinhVien.id != id, SinhVien.ma_sv == ma_sv).first()
    if sv:
        return jsonify({'duplicate': 'Mã sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien.query.filter(SinhVien.id != id, SinhVien.email == email).first()
    if sv:
        return jsonify({'duplicate': 'Email của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien.query.filter(SinhVien.id != id, SinhVien.phone == phone).first()
    if sv:
        return jsonify({'duplicate': 'Số điện thoại của sinh viên đã tồn tại. Không thể lưu sinh viên này.'})

    sv = SinhVien(**request.form)
    found_sv.ma_sv = sv.ma_sv
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
def deleteSinhVien(id):
    sv = SinhVien.query.get_or_404(id)
    if sv is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(sv)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Lớp Học------------------------------------------

@blueprint.route('/lop')
def lop():
    create_lop_form = CreateLopForm(request.form)
    # ky = Ky.query.all()
    # create_lop_form.mon_id.choices = dict([(row.ten_bomon, [(mon.id, mon.ma_mon + ' - ' + mon.ten_mon) for mon in row.mons]) for row in bomon])

    bomon = BoMon.query.all()
    create_lop_form.mon_id.choices = dict([(row.ten_bomon, [(mon.id, mon.ma_mon + ' - ' + mon.ten_mon) for mon in row.mons]) for row in bomon])

    create_lichlop_form = CreateLichLopForm(request.form)
    mon = Mon.query.all()
    create_lichlop_form.lop_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])
    bomon = BoMon.query.all()
    create_lichlop_form.gv_id.choices = dict([(row.ten_bomon, [(gv.id, gv.ma_gv+' - '+gv.last_name+' '+gv.first_name) for gv in row.gvs]) for row in bomon])
    create_lichlop_form.phong_id.choices = [(row.id, row.ten_phong) for row in Phong.query.all()]

    create_sv_lop_form = CreateSinhVien_LopForm(request.form)
    create_sv_lop_form.lop_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])
    sv = SinhVien.query.all()
    create_sv_lop_form.sv_id.choices = [(row.id, row.ma_sv+' - '+row.last_name+' '+row.first_name) for row in sv]
    
    return render_template('home/lop.html', segment='lop', forml=create_lop_form, formll=create_lichlop_form, formsv=create_sv_lop_form)

@blueprint.route('/lop', methods=['POST'])
def addLop():
    ten_lop = request.form['ten_lop']
    # lcn_id = request.form.getlist('lcn_id')

    lop = Lop.query.filter_by(ten_lop=ten_lop).first()
    if lop:
        return jsonify({'duplicate': 'Lớp học đã tồn tại. Không thể lưu lớp học này.'})


    lop = Lop(**request.form)
    # for row in lcn_id:
    #     lop.lcns.append(LopChuyenNganh.query.get(row))
    db.session.add(lop)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/lop/<int:id>', methods=['PUT'])
def updateLop(id):
    ten_lop = request.form['ten_lop']
    mon_id = int(request.form['mon_id'])
    # lcn_id = request.form.getlist('lcn_id')

    found_lop = Lop.query.filter_by(id=id).first()

    lop = Lop.query.filter(Lop.id != id, Lop.ten_lop == ten_lop).first()
    if lop:
        return jsonify({'duplicate': 'Lớp học đã tồn tại. Không thể lưu lớp học này.'})

    svs = SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == id).all()
    for sv in svs:
        lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv.sv_id, SinhVien_Lop.lop_id != id).all()
        for lop in lops:
            mon = Lop.query.filter(Lop.id == lop.lop_id).first()
            if mon.mon_id == mon_id:
                return jsonify({'duplicate': 'Lớp học này tồn tại sinh viên đã đăng ký học phần này. Không thể lưu lớp học này.'})


    lop = Lop(**request.form)
    found_lop.ten_lop = lop.ten_lop
    found_lop.so_luong = lop.so_luong
    found_lop.mon_id = lop.mon_id
    # found_lop.lcns = []

    # for row in lcn_id:
    #     found_lop.lcns.append(LopChuyenNganh.query.get(row))
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/lop/<int:id>', methods=['DELETE'])
def deleteLop(id):
    lop = Lop.query.get_or_404(id)
    if lop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(lop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Phòng Học------------------------------------------

@blueprint.route('/phong')
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
def deletePhong(id):
    phong = Phong.query.get_or_404(id)
    if phong is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(phong)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Lịch Lớp------------------------------------------

@blueprint.route('/lichlop')
def lichlop():
    create_lichlop_form = CreateLichLopForm(request.form)
    mon = Mon.query.all()
    create_lichlop_form.lop_id.choices = dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])
    bomon = BoMon.query.all()
    create_lichlop_form.gv_id.choices = dict([(row.ten_bomon, [(gv.id, gv.ma_gv+' - '+gv.last_name+' '+gv.first_name) for gv in row.gvs]) for row in bomon])
    create_lichlop_form.phong_id.choices = [(row.id, row.ten_phong) for row in Phong.query.all()]
    return render_template('home/lichlop.html', segment='lichlop', form=create_lichlop_form)

@blueprint.route('/lichlop', methods=['POST'])
def addLichLop():
    lop_id = int(request.form['lop_id'])
    thu = int(request.form['thu'])
    start = int(request.form['start'])
    end = int(request.form['end'])
    gv_id = request.form['gv_id']
    phong_id = request.form['phong_id']
    # lcn_id = request.form.getlist('lcn_id')

    lichlop = LichLop.query.filter(LichLop.thu == thu, LichLop.lop_id == lop_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
    if lichlop:
        return jsonify({'duplicate': 'Lịch lớp học bị trùng ca. Không thể lưu lịch lớp học này.'})

    lichlop = LichLop.query.filter(LichLop.thu == thu, LichLop.phong_id == phong_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
    if lichlop:
        return jsonify({'duplicate': 'Lịch lớp học bị trùng phòng. Không thể lưu lịch lớp học này.'})

    if gv_id != '':
        lichlop = LichLop.query.filter(LichLop.thu == thu, LichLop.gv_id == gv_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
        if lichlop:
            return jsonify({'duplicate': 'Giảng viên giảng dạy lớp này bị trùng lịch. Không thể lưu lịch lớp học này.'})

    svs = SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == lop_id).all()
    for sv in svs:
        lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv.sv_id, SinhVien_Lop.lop_id != lop_id).all()
        for lop in lops: 
            # if int(lop.lop_id) != lop_id:
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
def updateLichLop(id):
    lop_id = int(request.form['lop_id'])
    thu = int(request.form['thu'])
    start = int(request.form['start'])
    end = int(request.form['end'])
    gv_id = request.form['gv_id']
    phong_id = request.form['phong_id']

    found_lichlop = LichLop.query.filter_by(id=id).first()

    lichlop = LichLop.query.filter(LichLop.id != id, LichLop.thu == thu, LichLop.lop_id == lop_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
    if lichlop:
        return jsonify({'duplicate': 'Lịch lớp học bị trùng ca. Không thể lưu lịch lớp học này.'})

    lichlop = LichLop.query.filter(LichLop.id != id, LichLop.thu == thu, LichLop.phong_id == phong_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
    if lichlop:
        return jsonify({'duplicate': 'Lịch lớp học bị trùng phòng. Không thể lưu lịch lớp học này.'})

    if gv_id != '':
        lichlop = LichLop.query.filter(LichLop.id != id, LichLop.thu == thu, LichLop.gv_id == gv_id, or_(and_(LichLop.start <= start, start <= LichLop.end), and_(LichLop.start <= end, end <= LichLop.end))).first()
        if lichlop:
            return jsonify({'duplicate': 'Giảng viên giảng dạy lớp này bị trùng lịch. Không thể lưu lịch lớp học này.'})

    svs = SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == lop_id).all()
    for sv in svs:
        lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv.sv_id, SinhVien_Lop.lop_id != lop_id).all()
        for lop in lops: 
            # if int(lop.lop_id) != lop_id:
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
def deleteLichLop(id):
    lichlop = LichLop.query.get_or_404(id)
    if lichlop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(lichlop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Sinh Viên - Lớp------------------------------------------

@blueprint.route('/sv_lop', methods=['POST'])
def addSVLop():
    lop_id = int(request.form['lop_id'])
    sv_id = int(request.form['sv_id'])

    lichlop1 = LichLop.query.filter(LichLop.lop_id == lop_id).all()
    mon1 = Lop.query.filter(Lop.id == lop_id).first()

    lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id).all()

    for lop in lops:
        mon2 = Lop.query.filter(Lop.id == lop.lop_id).first()
        if mon1.mon_id == mon2.mon_id:
            return jsonify({'duplicate': 'Sinh viên này đã đăng ký học phần này. Không thể thêm sinh viên này.'})

    for lop in lops:
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
def deleteSVLop(id):
    sv_lop = SinhVien_Lop.query.get_or_404(id)
    if sv_lop is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(sv_lop)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})



#-------------------------------------Năm Học------------------------------------------

@blueprint.route('/nam')
def nam():
    create_nam_form = CreateNamForm(request.form)
    return render_template('home/nam.html', segment='nam', formn=create_nam_form)

@blueprint.route('/nam', methods=['POST'])
def addNam():
    # namhoc = request.form['namhoc']
    hk1 = request.form['hk1']
    hk2 = request.form['hk2']
    hk3 = request.form['hk3']
    date_end = request.form['date_end']

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
def updateNam(id):
    hk1 = request.form['hk1']
    hk2 = request.form['hk2']
    hk3 = request.form['hk3']
    date_end = request.form['date_end']

    found_nam = Nam.query.filter_by(id=id).first()

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
def deleteNam(id):
    nam = Nam.query.get_or_404(id)
    if nam is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(nam)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})


#-------------------------------------Kỳ Học------------------------------------------

# @blueprint.route('/ky')
# def ky():
#     create_ky_form = CreateKyForm(request.form)
#     return render_template('home/ky.html', segment='ky', form=create_ky_form)

@blueprint.route('/ky', methods=['POST'])
def addKy():
    nam_id = request.form['nam_id']
    ten_ky = request.form['ten_ky']

    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ten_ky).first()
    if ky:
        return jsonify({'duplicate': 'Kỳ học đã tồn tại. Không thể lưu kỳ học này.'})

    ky = Ky(**request.form)
    db.session.add(ky)
    db.session.commit()
        
    return jsonify({'success': 'Thêm thành công.'})

@blueprint.route('/ky/<int:id>', methods=['PUT'])
def updateKy(id):
    nam_id = request.form['nam_id']
    ten_ky = request.form['ten_ky']

    found_ky = Ky.query.filter_by(id=id).first()

    ky = Ky.query.filter(Ky.id != id, Ky.nam_id == nam_id, Ky.ten_ky == ten_ky).first()
    if ky:
        return jsonify({'duplicate': 'Năm học đã tồn tại. Không thể lưu năm học này.'})

    ky = Ky(**request.form)
    found_ky.nam_id = ky.nam_id
    found_ky.ten_ky = ky.ten_ky
    db.session.commit()
        
    return jsonify({'success': 'Cập nhật thành công.'})

@blueprint.route('/ky/<int:id>', methods=['DELETE'])
def deleteKy(id):
    ky = Ky.query.get_or_404(id)
    if ky is None:
        return jsonify({'error': 'Không tìm thấy.'})
    db.session.delete(ky)
    db.session.commit()
    return jsonify({'success': 'Xóa thành công.'})





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

@blueprint.route('/user', methods=['GET', 'POST'])
def user():
    users = Users.query.all()
    return render_template('home/user.html', segment='user', users=users)

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