# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

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
from apps.authentication.models import Khoa, Nganh, Mon, Users, ChuongTrinhDaoTao

from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))



# Api
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
