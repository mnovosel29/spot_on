import base64
import os

import flask_login
from PIL import Image
from flask_babel import gettext
from flask_security import verify_password, hash_password, login_required
from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename

from app.models.avatar import Avatar
from app.routes.auth.forms import ProfileForm, EmailForm, ChangePasswordForm, AvatarForm, AvatarDeleteForm
from app.routes.auth import bp
from app.extensions import db
from app.models.auth import User


@bp.route('/profile')
@login_required
def profile():
    if flask_login.current_user.is_authenticated:
        user = User.query.get(flask_login.current_user.id)
    else:
        user = None
    name_form = ProfileForm(obj=user)
    email_form = EmailForm(obj=user)
    change_password_form = ChangePasswordForm()
    avatar_form = AvatarForm(obj=user)
    avatar_delete_form = AvatarDeleteForm(obj=user)
    return render_template('auth/profile.html',
                           name_form=name_form,
                           email_form=email_form,
                           change_password_form=change_password_form,
                           avatar_form=avatar_form,
                           avatar_delete_form=avatar_delete_form,
                           user=user
                           )


@bp.route('/profile/name', methods=['POST'])
@login_required
def profile_name():
    if flask_login.current_user.is_authenticated:
        user = User.query.get(flask_login.current_user.id)
    else:
        user = None
    name_form = ProfileForm(request.form)
    email_form = EmailForm(obj=user)
    change_password_form = ChangePasswordForm()
    avatar_form = AvatarForm(obj=user)
    avatar_delete_form = AvatarDeleteForm(obj=user)
    if name_form.validate_on_submit():
        name_form.populate_obj(user)
        db.session.commit()
        flash(gettext('Profile updated successfully'), 'success')
        return redirect(url_for('auth.profile'))
    return render_template('auth/profile.html',
                           name_form=name_form,
                           email_form=email_form,
                           change_password_form=change_password_form,
                           avatar_form=avatar_form,
                           avatar_delete_form=avatar_delete_form,
                           user=user
                           )


@bp.route('/profile/email', methods=['POST'])
@login_required
def profile_email():
    if flask_login.current_user.is_authenticated:
        user = User.query.get(flask_login.current_user.id)
    else:
        user = None

    name_form = ProfileForm(obj=user)
    email_form = EmailForm(request.form)
    change_password_form = ChangePasswordForm()
    avatar_form = AvatarForm(obj=user)
    avatar_delete_form = AvatarDeleteForm(obj=user)
    if email_form.validate_on_submit():
        if User.query.filter_by(email=email_form.email.data).first() is None:
            email_form.populate_obj(user)
            db.session.commit()
            flash(gettext('Email updated successfully.'), 'success')

    return render_template('auth/profile.html',
                           name_form=name_form,
                           email_form=email_form,
                           change_password_form=change_password_form,
                           avatar_form=avatar_form,
                           avatar_delete_form=avatar_delete_form,
                           user=user
                           )


@bp.route('/profile/password', methods=['POST'])
@login_required
def profile_password():
    if flask_login.current_user.is_authenticated:
        user = User.query.get(flask_login.current_user.id)
    else:
        user = None
    name_form = ProfileForm(obj=user)
    email_form = EmailForm(obj=user)
    change_password_form = ChangePasswordForm(request.form)
    avatar_form = AvatarForm(obj=user)
    avatar_delete_form = AvatarDeleteForm(obj=user)
    if change_password_form.validate_on_submit():
        if not verify_password(change_password_form.current_password.data, user.password):
            change_password_form.current_password.errors.append(gettext('Incorrect current password'))
        else:
            user.password = hash_password(change_password_form.password.data)
            db.session.commit()
            flash(gettext('Password updated successfully.'), 'success')
            return redirect(url_for('auth.profile'))
    return render_template('auth/profile.html',
                           name_form=name_form,
                           email_form=email_form,
                           change_password_form=change_password_form,
                           avatar_form=avatar_form,
                           avatar_delete_form=avatar_delete_form,
                           user=user
                           )


@bp.route('/profile/update_avatar', methods=['POST'])
@login_required
def update_avatar():
    if flask_login.current_user.is_authenticated:
        user = User.query.get(flask_login.current_user.id)
    else:
        user = None
    name_form = ProfileForm(obj=user)
    email_form = EmailForm(obj=user)
    change_password_form = ChangePasswordForm()
    avatar_form = AvatarForm(obj=user)
    avatar_delete_form = AvatarDeleteForm(obj=user)
    if avatar_form.validate_on_submit():
        avatar = avatar_form.avatar.data
        if avatar:
            filename = secure_filename(avatar.filename)
            avatar_path = os.path.join('app/static/temp', filename)
            avatar.save(avatar_path)
            avatar = Image.open(avatar_path)
            avatar.thumbnail((75, 75))
            avatar.save(avatar_path)

            with open(avatar_path, 'rb') as f:
                base64_avatar = base64.b64encode(f.read()).decode('utf-8')

            if user.avatar:
                user.avatar.image = base64_avatar
                db.session.add(user.avatar)
            else:
                new_avatar = Avatar()
                new_avatar.image = base64_avatar
                new_avatar.user_id = user.id
                db.session.add(new_avatar)

            db.session.commit()
            flash(gettext('Avatar updated successfully.'), 'success')

            os.remove(avatar_path)

    return render_template('auth/profile.html',
                           name_form=name_form,
                           email_form=email_form,
                           change_password_form=change_password_form,
                           avatar_form=avatar_form,
                           avatar_delete_form=avatar_delete_form,
                           user=user
                           )


@bp.route('/profile/delete_avatar', methods=['POST'])
@login_required
def delete_avatar():
    if flask_login.current_user.is_authenticated:
        user = User.query.get(flask_login.current_user.id)
    else:
        user = None
    name_form = ProfileForm(obj=user)
    email_form = EmailForm(obj=user)
    change_password_form = ChangePasswordForm()
    avatar_form = AvatarForm(obj=user)
    avatar_delete_form = AvatarDeleteForm(obj=user)
    if avatar_delete_form.validate_on_submit():
        if user.avatar:
            db.session.delete(user.avatar)
            db.session.commit()
            flash(gettext('Avatar deleted successfully.'), 'success')
        else:
            flash(gettext('No avatar to delete.'), 'error')

    return render_template('auth/profile.html',
                           name_form=name_form,
                           email_form=email_form,
                           change_password_form=change_password_form,
                           avatar_form=avatar_form,
                           avatar_delete_form=avatar_delete_form,
                           user=user
                           )

