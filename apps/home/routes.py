# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from re import S
from apps.authentication.forms import CreateKhoaForm, CreateNganhForm, CreateMonForm, CreateChuongTrinhDaoTaoForm
from apps.authentication.models import Khoa, Nganh, Mon, ChuongTrinhDaoTao, ChuongTrinhDaoTao_MonHoc, Users
from apps.home import blueprint
from apps import db, login_manager, create_app
from flask import Flask, render_template, jsonify, redirect, request, session, url_for, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
# import cv2
# import dlib
# import numpy as np
# import os
# from PIL import Image

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


#-------------------------------------Môn học------------------------------------------

@blueprint.route('/mon')
def mon():
    create_mon_form = CreateMonForm(request.form)
    khoa =  Khoa.query.all()
    # select_field = {}
    # for nganh in khoa:
    #     select_field.append(nganh.ten_khoa)
    #     [(row.id, row.ten_nganh) for row in nganh.nganhs]
    # create_mon_form.nganh_id.choices = select_field
    create_mon_form.nganh_id.choices = dict([(nganh.ten_khoa, [(row.id, row.ten_nganh) for row in nganh.nganhs]) for nganh in khoa])
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
    found_mon.nganh_id = mon.nganh_id
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
    create_ctdt_form.nganh_id.choices = dict([(nganh.ten_khoa, [(row.id, row.ten_nganh) for row in nganh.nganhs]) for nganh in khoa])
    nganh = Nganh.query.all()
    create_ctdt_form.mon_id.choices = dict([(mon.ten_nganh, [(row.id, row.ten_mon) for row in mon.mons]) for mon in nganh])
    return render_template('home/chuongtrinhdaotao.html', segment='chuongtrinhdaotao', form=create_ctdt_form)

@blueprint.route('/chuongtrinhdaotao', methods=['POST'])
def addChuongTrinhDaoTao():
    ma_ctdt = request.form['ma_ctdt']
    ten_ctdt = request.form['ten_ctdt']
    mon_id = request.form.getlist('mon_id')

    ctdt = ChuongTrinhDaoTao.query.filter_by(ma_ctdt=ma_ctdt).first()
    if ctdt:
        return jsonify({'duplicate': 'Mã môn đã tồn tại. Không thể lưu môn này.'})

    ctdt = ChuongTrinhDaoTao.query.filter_by(ten_ctdt=ten_ctdt).first()
    if ctdt:
        return jsonify({'duplicate': 'Tên môn đã tồn tại. Không thể lưu môn này.'})

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
        return jsonify({'duplicate': 'Mã môn đã tồn tại. Không thể lưu môn này.'})

    ctdt = ChuongTrinhDaoTao.query.filter(ChuongTrinhDaoTao.id != id, ChuongTrinhDaoTao.ten_ctdt == ten_ctdt).first()
    if ctdt:
        return jsonify({'duplicate': 'Tên môn đã tồn tại. Không thể lưu môn này.'})

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