# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from codecs import BOM
from flask import jsonify, render_template, redirect, request, url_for
import pandas as pd
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import BoMon, Khoa, Nganh, Mon, SinhVien_Lop, Users, ChuongTrinhDaoTao, GiangVien, LopChuyenNganh, SinhVien, Lop, Phong, LichLop

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))



# -------------------------------------------------API--------------------------------------------------------
# -------------------------Khoa--------------------------------
@blueprint.route('/api/khoa', methods=['POST'])
def dataKhoa():
    return jsonify({'data': [khoa.to_dict() for khoa in Khoa.query.all()]})

@blueprint.route('/api/khoa/info', methods=['POST'])
def dataKhoaInfo():
    if 'id' in request.form:
        id = request.form['id']
        khoa = Khoa.query.filter_by(id=id).first()
        return jsonify({'data': khoa.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})

# -------------------------Nganh--------------------------------
@blueprint.route('/api/nganh', methods=['POST'])
def dataNganh():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [nganh.to_dict() for nganh in Nganh.query.all()]})

@blueprint.route('/api/nganh/info', methods=['POST'])
def dataNganhInfo():
    if 'id' in request.form:
        id = request.form['id']
        nganh = Nganh.query.filter_by(id=id).first()
        return jsonify({'data': nganh.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------BoMon--------------------------------
@blueprint.route('/api/bomon', methods=['POST'])
def dataBoMon():
    return jsonify({'data': [bomon.to_dict() for bomon in BoMon.query.all()]})

@blueprint.route('/api/bomon/info', methods=['POST'])
def dataBoMonInfo():
    if 'id' in request.form:
        id = request.form['id']
        bomon = BoMon.query.filter_by(id=id).first()
        return jsonify({'data': bomon.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------Mon--------------------------------
@blueprint.route('/api/mon', methods=['POST'])
def dataMon():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [mon.to_dict() for mon in Mon.query.all()]})

@blueprint.route('/api/mon/info', methods=['POST'])
def dataMonInfo():
    if 'id' in request.form:
        id = request.form['id']
        mon = Mon.query.filter_by(id=id).first()
        return jsonify({'data': mon.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------ChuongTrinhDaoTao--------------------------------
@blueprint.route('/api/ctdt', methods=['POST'])
def dataChuongTrinhDaoTao():
    return jsonify({'data': [ctdt.to_dict() for ctdt in ChuongTrinhDaoTao.query.all()]})

@blueprint.route('/api/ctdt/info', methods=['POST'])
def dataChuongTrinhDaoTaoInfo():
    if 'id' in request.form:
        id = request.form['id']
        ctdt = ChuongTrinhDaoTao.query.filter_by(id=id).first()
        return jsonify({'data': ctdt.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------GiangVien--------------------------------
@blueprint.route('/api/giangvien', methods=['POST'])
def dataGiangVien():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [gv.to_dict() for gv in GiangVien.query.all()]})

@blueprint.route('/api/giangvien/info', methods=['POST'])
def dataGiangVienInfo():
    if 'id' in request.form:
        id = request.form['id']
        gv = GiangVien.query.filter_by(id=id).first()
        return jsonify({'data': gv.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------LopChuyenNganh--------------------------------
@blueprint.route('/api/lcn', methods=['POST'])
def dataLopChuyenNganh():
    return jsonify({'data': [lcn.to_dict() for lcn in LopChuyenNganh.query.all()]})

@blueprint.route('/api/lcn/info', methods=['POST'])
def dataLopChuyenNganhInfo():
    if 'id' in request.form:
        id = request.form['id']
        lcn = LopChuyenNganh.query.filter_by(id=id).first()
        return jsonify({'data': lcn.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------SinhVien--------------------------------
@blueprint.route('/api/sinhvien', methods=['POST'])
def dataSinhVien():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [sv.to_dict() for sv in SinhVien.query.all()]})

@blueprint.route('/api/sinhvien/lop/<int:lop_id>', methods=['POST'])
def dataSinhVien_LopHoc(lop_id):
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)

    return jsonify({'data': [sv.to_dict() for sv in SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == lop_id).all()]})

@blueprint.route('/api/sinhvien/info', methods=['POST'])
def dataSinhVienInfo():
    if 'id' in request.form:
        id = request.form['id']
        sv = SinhVien.query.filter_by(id=id).first()
        return jsonify({'data': sv.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})



# -------------------------LopHoc--------------------------------
@blueprint.route('/api/lop', methods=['POST'])
def dataLop():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [lop.to_dict() for lop in Lop.query.all()]})


@blueprint.route('/api/select/lop', methods=['GET'])
def selectLop():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'results': [{
                                'id': lop.id, 
                                'text': lop.ten_lop
                            } for lop in Lop.query.all()]
                    })
    # dict([(row.ma_mon + ' - ' + row.ten_mon, [(lop.id, lop.ten_lop) for lop in row.lops]) for row in mon])

@blueprint.route('/api/lop/info', methods=['POST'])
def dataLopInfo():
    if 'id' in request.form:
        id = request.form['id']
        lop = Lop.query.filter_by(id=id).first()
        return jsonify({'data': lop.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------PhongHoc--------------------------------
@blueprint.route('/api/phong', methods=['POST'])
def dataPhong():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [phong.to_dict() for phong in Phong.query.all()]})

@blueprint.route('/api/phong/info', methods=['POST'])
def dataPhongInfo():
    if 'id' in request.form:
        id = request.form['id']
        phong = Phong.query.filter_by(id=id).first()
        return jsonify({'data': phong.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------LichLop--------------------------------
@blueprint.route('/api/lichlop', methods=['POST'])
def dataLichLop():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [lichlop.to_dict() for lichlop in LichLop.query.all()]})

@blueprint.route('/api/lichlop/<int:id>', methods=['POST'])
def dataLichLopById(id):
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [lichlop.to_dict() for lichlop in LichLop.query.filter(LichLop.lop_id == id).all()]})

@blueprint.route('/api/lichlop/info', methods=['POST'])
def dataLichLopInfo():
    if 'id' in request.form:
        id = request.form['id']
        lichlop = LichLop.query.filter_by(id=id).first()
        return jsonify({'data': lichlop.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})



# -------------------------Test Api--------------------------------
@blueprint.route('/test/api/khoa/<int:id>/<string:ten_khoa>')
def testDataKhoa(id, ten_khoa):
    return jsonify({'data': ''})



# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        
        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/profile')
def profile():
    user = Users(**request.form)
    return render_template('accounts/profile.html',
                                   msg='User Profile',
                                   user=current_user)

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
