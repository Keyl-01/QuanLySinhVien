# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from codecs import BOM
import datetime
import json
from tabnanny import check
from flask import jsonify, render_template, redirect, request, session, url_for
import pandas as pd
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Person, BoMon, Khoa, Nganh, Mon, SinhVien_Lop, NhanVien, ChuongTrinhDaoTao, GiangVien, LopChuyenNganh, SinhVien, Lop, Phong, LichLop, Nam, Ky, LichThi, SinhVien_LichThi

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))



# -------------------------------------------------API--------------------------------------------------------
# -------------------------NhanVien--------------------------------
@blueprint.route('/api/nhanvien', methods=['POST'])
def dataNhanVien():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [nv.to_dict() for nv in NhanVien.query.all()]})

@blueprint.route('/api/nhanvien/info', methods=['POST'])
def dataNhanVienInfo():
    if 'id' in request.form:
        id = request.form['id']
        nv = NhanVien.query.filter_by(id=id).first()
        return jsonify({'data': nv.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


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

@blueprint.route('/api/select/ctdt/<int:nganh_id>', methods=['GET'])
def selectChuongTrinhDaoTao(nganh_id):
    return jsonify({'data': [ctdt.to_dict() for ctdt in ChuongTrinhDaoTao.query.filter(ChuongTrinhDaoTao.nganh_id == nganh_id).all()]})

@blueprint.route('/api/ctdt/<int:ctdt_id>', methods=['GET'])
def dataChuongTrinhDaoTaoMon(ctdt_id):
    ctdt = ChuongTrinhDaoTao.query.filter(ChuongTrinhDaoTao.id == ctdt_id).first()
    # ctdt.mons.
    # print(mon)
    # mons = ctdt.mons if n == 10 else ''
    return jsonify({'data': [mon.to_dict() for mon in ctdt.mons]})

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



# -------------------------DiemSinhVien--------------------------------
@blueprint.route('/api/diemsv/<int:sv_id>', methods=['GET'])
def dataDiemSinhVien(sv_id):
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    sv = SinhVien.query.filter(SinhVien.id == sv_id).first()
    return jsonify(sv.to_dictDiem())

@blueprint.route('/api/diemsv/<int:sv_id>/<int:nam_id>/<int:ky_id>', methods=['GET'])
def dataDiemSinhVienCT(sv_id, nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    sv = SinhVien.query.filter(SinhVien.id == sv_id).first()
    return jsonify(sv.to_dictDiemCT(ky.id))


# -------------------------LopHoc--------------------------------
@blueprint.route('/api/lop', methods=['POST'])
def dataLop():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [lop.to_dict() for lop in Lop.query.all()]})

@blueprint.route('/api/lop/<int:nam_id>/<int:ky_id>', methods=['GET'])
def dataLopFilter(nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [lop.to_dict() for lop in Lop.query.filter(Lop.ky_id == ky.id).all()]})

@blueprint.route('/api/select/lop', methods=['GET'])
def selectLop():
    return jsonify({'results': [{
                                'id': lop.id, 
                                'text': lop.ten_lop
                            } for lop in Lop.query.all()]
                    })

# @blueprint.route('/api/select/lop/<int:nam_id>/<int:ky_id>', methods=['GET'])
# def selectLopKy(nam_id, ky_id):
#     ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
#     return jsonify({'results': [{
#                                 'id': lop.id, 
#                                 'text': lop.ten_lop
#                             } for lop in Lop.query.filter(Lop.ky_id == ky.id).all()]
#                     })


@blueprint.route('/api/select/lop/<int:nam_id>/<int:ky_id>', methods=['GET'])
def selectLopKy(nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    return jsonify({'data': [lop.to_dict() for lop in Lop.query.filter(Lop.ky_id == ky.id).all()]})

@blueprint.route('/api/select/lop/<int:nam_id>/<int:ky_id>/<int:gv_id>', methods=['GET'])
def selectLopKyByGV(nam_id, ky_id, gv_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    lops = Lop.query.filter(Lop.ky_id == ky.id).all()
    result = []
    for lop in lops:
        for lichlop in lop.lichlops:
            if lichlop.gv_id == gv_id:
                result.append(lop)
                break

    return jsonify({'data': [lop.to_dict() for lop in result]})

@blueprint.route('/api/lop/info', methods=['POST'])
def dataLopInfo():
    if 'id' in request.form:
        id = request.form['id']
        lop = Lop.query.filter_by(id=id).first()
        return jsonify({'data': lop.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})



# -------------------------SinhVien_Lop--------------------------------

@blueprint.route('/api/sv_lop/<int:lop_id>', methods=['GET'])
def dataSVLopFilter(lop_id):
    return jsonify({'data': [sv.to_dict() for sv in SinhVien_Lop.query.filter(SinhVien_Lop.lop_id == lop_id).all()]})

@blueprint.route('/api/sv_lop/info', methods=['POST'])
def dataSVLopInfo():
    if 'id' in request.form:
        id = request.form['id']
        sv_lop = SinhVien_Lop.query.filter_by(id=id).first()
        return jsonify({'data': sv_lop.to_dict()})
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


@blueprint.route('/api/lichlop/<int:nam_id>/<int:ky_id>', methods=['GET'])
def dataLichLopFilter(nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    lops = Lop.query.filter(Lop.ky_id == ky.id).all()
    lichlops = []
    for lop in lops:
        for lichlop in LichLop.query.filter(LichLop.lop_id == lop.id).all():
            lichlops.append(lichlop)
    return jsonify({'data': [lichlop.to_dict() for lichlop in lichlops]})


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



@blueprint.route('/api/lichlop/giangvien/<int:gv_id>/<int:nam_id>/<int:ky_id>', methods=['GET'])
def dataTKBGVFilter(gv_id, nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    lops = Lop.query.filter(Lop.ky_id == ky.id).all()
    lichlops = []
    for lop in lops:
        for lichlop in LichLop.query.filter(LichLop.lop_id == lop.id, LichLop.gv_id == gv_id).all():
            lichlops.append(lichlop)
    return jsonify({'data': [lichlop.to_dict() for lichlop in lichlops]})


@blueprint.route('/api/lichlop/sinhvien/<int:sv_id>/<int:nam_id>/<int:ky_id>', methods=['GET'])
def dataTKBSVFilter(sv_id, nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    lops = Lop.query.filter(Lop.ky_id == ky.id).all()
    sv_lops = SinhVien_Lop.query.filter(SinhVien_Lop.sv_id == sv_id).all()
    lichlops = []
    for lop in lops:
        for sv_lop in sv_lops:
            if lop.id == sv_lop.lop_id:
                for lichlop in LichLop.query.filter(LichLop.lop_id == lop.id).all():
                    lichlops.append(lichlop)
    return jsonify({'data': [lichlop.to_dict() for lichlop in lichlops]})


# -------------------------NamHoc--------------------------------
@blueprint.route('/api/nam', methods=['POST'])
def dataNam():
    return jsonify({'data': [nam.to_dict() for nam in Nam.query.all()]})

@blueprint.route('/api/select/nam', methods=['GET'])
def selectNam():
    return jsonify({'results': [{
                                'id': nam.id, 
                                'text': nam.start + ' - ' + nam.end
                            } for nam in Nam.query.all()]
                    })

@blueprint.route('/api/nam/info', methods=['POST'])
def dataNamInfo():
    if 'id' in request.form:
        id = request.form['id']
        nam = Nam.query.filter_by(id=id).first()
        return jsonify({'data': nam.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


# -------------------------KyHoc--------------------------------
@blueprint.route('/api/ky', methods=['POST'])
def dataKy():
    return jsonify({'data': [ky.to_dict() for ky in Ky.query.all()]})

@blueprint.route('/api/ky/<int:ky_id>', methods=['GET'])
def dataKyInfo(ky_id):
    ky = Ky.query.filter_by(id = ky_id).first()
    return jsonify({'data': ky.to_dict()})
    # if 'id' in request.form:
    #     id = request.form['id']
    #     ky = Ky.query.filter_by(id=id).first()
    #     return jsonify({'data': ky.to_dict()})
    # return jsonify({'error': 'Không tồn tại dữ liệu này.'})



# -------------------------LichThi--------------------------------
@blueprint.route('/api/lichthi', methods=['POST'])
def dataLichThi():
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [lichthi.to_dict() for lichthi in LichThi.query.all()]})

@blueprint.route('/api/lichthi/<int:nam_id>/<int:ky_id>', methods=['GET'])
def dataLichThiFilter(nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    # data = db.session.query(Nganh, Khoa).join(Nganh, Khoa.id == Nganh.khoa_id)
    return jsonify({'data': [lichthi.to_dict() for lichthi in LichThi.query.filter(LichThi.ky_id == ky.id).all()]})

@blueprint.route('/api/select/lichthi', methods=['GET'])
def selectLichThi():
    return jsonify({'results': [{
                                'id': lichthi.id, 
                                'text': lichthi.mon.ten_mon
                            } for lichthi in LichThi.query.all()]
                    })

@blueprint.route('/api/select/lichthi/<int:nam_id>/<int:ky_id>', methods=['GET'])
def selectLichThiKy(nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    return jsonify({'data': [lichthi.to_dict() for lichthi in LichThi.query.filter(LichThi.ky_id == ky.id).all()]})

@blueprint.route('/api/lichthi/info', methods=['POST'])
def dataLichThiInfo():
    if 'id' in request.form:
        id = request.form['id']
        lichthi = LichThi.query.filter_by(id=id).first()
        return jsonify({'data': lichthi.to_dict()})
    return jsonify({'error': 'Không tồn tại dữ liệu này.'})


@blueprint.route('/api/select/sv_lichthi/<int:mon_id>/<int:nam_id>/<int:ky_id>', methods=['GET'])
def selectSV_LichThi(mon_id, nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    svs = []
    lops = Lop.query.filter(Lop.ky_id <= ky.id, Lop.mon_id == mon_id).all()
    for lop in lops:
        for sv in lop.sv_ls:
            if sv.diemQT is not None:
                if sv.diemQT >= 4.0:
                    if sv.sinhvien not in svs:
                        svs.append(sv.sinhvien)
    return jsonify({'results': [{
                                'id': sv.id, 
                                'text': sv.pcode + ' - ' + sv.last_name + ' ' + sv.first_name
                            } for sv in svs]
                    })


@blueprint.route('/api/lichthi/<int:sv_id>/<int:nam_id>/<int:ky_id>', methods=['GET'])
def dataLichThiSVFilter(sv_id, nam_id, ky_id):
    ky = Ky.query.filter(Ky.nam_id == nam_id, Ky.ten_ky == ky_id).first()
    lichthis = LichThi.query.filter(LichThi.ky_id == ky.id).all()
    sv_lichthis = []
    for lichthi in lichthis:
        for sv_lichthi in lichthi.sv_lichthis:
            if sv_lichthi.sv_id == sv_id:
                sv_lichthis.append(lichthi)
                break
    return jsonify({'data': [lichthi.to_dict() for lichthi in sv_lichthis]})

# -------------------------SinhVien_LichThi--------------------------------

@blueprint.route('/api/sv_lichthi/<int:lichthi_id>', methods=['GET'])
def dataSVLichThiFilter(lichthi_id):
    return jsonify({'data': [sv.to_dict() for sv in SinhVien_LichThi.query.filter(SinhVien_LichThi.lichthi_id == lichthi_id).all()]})

@blueprint.route('/api/sv_lichthi/info', methods=['POST'])
def dataSVLichThiInfo():
    if 'id' in request.form:
        id = request.form['id']
        sv_lichthi = SinhVien_LichThi.query.filter_by(id=id).first()
        return jsonify({'data': sv_lichthi.to_dict()})
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
        person = Person.query.filter_by(username=username).first()
        # Check the password
        if person:
            if person.password:
                if verify_pass(password, person.password):
                    login_user(person)
                    return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)
                               
    if current_user.is_authenticated:
        if current_user.role == 1:
            if current_user.type == 1:# Phong Dao tao
                return redirect(url_for('home_blueprint.index'))
            if current_user.type == 2: # Phong Cong tac HSSV
                return redirect(url_for('home_blueprint.profileNVHSSV'))
        if current_user.role == 3: # Giang vien
            return redirect(url_for('home_blueprint.tkbGV'))
        if current_user.role == 4: # Sinh vien
            return redirect(url_for('home_blueprint.tkbSV'))
    
    return render_template('accounts/login.html',
                            form=login_form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        
        # Check usename exists
        person = Person.query.filter_by(username=username).first()
        if person:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        person = Person.query.filter_by(email=email).first()
        if person:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        nv = NhanVien(**request.form)
        # nv.pcode = 'admin'
        # nv.first_name = 'Cường'
        # nv.last_name = 'Nguyễn'
        # nv.date_birth = datetime.datetime.now()
        # nv.phone = '0868235001'
        # nv.type = 1
        db.session.add(nv)
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
