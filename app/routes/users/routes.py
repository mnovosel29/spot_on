import os
import base64
from datetime import datetime
import uuid
from PIL import Image

from flask import render_template, request, flash, redirect, url_for
from flask_babel import gettext
from flask_security import hash_password, roles_required
from werkzeug.utils import secure_filename

from app.models.avatar import Avatar
from app.routes.users.forms import (
    UserCreateForm,
    UserInfoForm,
    UserEmailForm,
    UserPasswordForm,
    UserRolesForm,
    UserActivateForm,
    UserDeactivateForm,
    UserConfirmForm,
    UserDeleteForm,
    UserAvatarForm,
    UserAvatarDeleteForm
)
from app.routes.users import bp
from app.extensions import db
from app.models.auth import User, Role


def _initialize_forms(user):
    roles = Role.query.all()
    forms = {
        'user_info_form': UserInfoForm(obj=user),
        'user_email_form': UserEmailForm(obj=user),
        'user_password_form': UserPasswordForm(obj=user),
        'user_avatar_form': UserAvatarForm(obj=user),
        'user_avatar_delete_form': UserAvatarDeleteForm(obj=user),
        'user_roles_form': UserRolesForm(obj=user),
        'user_activate_form': UserActivateForm(obj=user),
        'user_deactivate_form': UserDeactivateForm(obj=user),
        'user_confirm_form': UserConfirmForm(obj=user),
        'user_delete_form': UserDeleteForm(obj=user)
    }
    forms['user_roles_form'].roles.choices = [(role.id, role.name) for role in roles]
    forms['user_roles_form'].roles.data = [role.id for role in user.roles]

    for form_name, form in forms.items():
        form.validate_on_submit()

    return forms


@bp.route('/', methods=('GET', 'POST'))
@roles_required('Admin')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    users = User.query.paginate(page=page, per_page=per_page)

    return render_template('admin/users/index.html', users=users)


@bp.route('/create', methods=['GET', 'POST'])
@roles_required('Admin')
def create():
    user_create_form = UserCreateForm()
    if user_create_form.validate_on_submit():
        new_user = User()
        new_user.first_name = user_create_form.first_name.data
        new_user.last_name = user_create_form.last_name.data
        new_user.email = user_create_form.email.data
        new_user.password = hash_password(user_create_form.password.data)
        new_user.fs_uniquifier = str(uuid.uuid4().hex)
        new_user.active = True
        db.session.add(new_user)
        db.session.commit()
        flash(gettext('User created successfully.'), 'success')
        return redirect(url_for('users.index'))
    return render_template('admin/users/create.html', user_create_form=user_create_form)


@bp.route('/<int:user_id>')
@roles_required('Admin')
def detail(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)

    return render_template('admin/users/detail.html',
                           user=user,
                           roles=Role.query.all(),
                           **forms
                           )


@bp.route('/<int:user_id>/update_info', methods=['POST'])
@roles_required('Admin')
def update_info(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_info_form = forms['user_info_form']
    if user_info_form.validate_on_submit():
        user.first_name = user_info_form.first_name.data
        user.last_name = user_info_form.last_name.data
        db.session.commit()
        flash(gettext('User information updated successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/update_email', methods=['POST'])
@roles_required('Admin')
def update_email(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_email_form = forms['user_email_form']
    if user_email_form.validate_on_submit():
        if User.query.filter(User.email == user_email_form.email.data).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('users.detail', user_id=user_id))
        user.email = user_email_form.email.data
        user.fs_uniquifier = str(uuid.uuid4().hex)
        db.session.commit()
        flash(gettext('Email updated successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/update_password', methods=['POST'])
@roles_required('Admin')
def update_password(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_password_form = forms['user_password_form']
    if user_password_form.validate_on_submit():
        user.password = hash_password(user_password_form.password.data)
        user.fs_uniquifier = str(uuid.uuid4().hex)
        db.session.commit()
        flash(gettext('Password updated successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/delete_avatar', methods=['POST'])
@roles_required('Admin')
def delete_avatar(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_avatar_delete_form = forms['user_avatar_delete_form']
    if user_avatar_delete_form.validate_on_submit():
        if user.avatar:
            db.session.delete(user.avatar)
            db.session.commit()
            flash(gettext('Avatar deleted successfully.'), 'success')
        else:
            flash(gettext('No avatar to delete.'), 'error')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/update_avatar', methods=['POST'])
@roles_required('Admin')
def update_avatar(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_avatar_form = forms['user_avatar_form']
    if user_avatar_form.validate_on_submit():
        avatar = user_avatar_form.avatar.data
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
                new_avatar.user_id = user_id
                db.session.add(new_avatar)

            db.session.commit()
            flash(gettext('Avatar updated successfully.'), 'success')

            os.remove(avatar_path)
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/update_roles', methods=['POST'])
@roles_required('Admin')
def update_roles(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_roles_form = forms['user_roles_form']
    if user_roles_form.validate_on_submit():
        user.roles = []
        for data in user_roles_form.roles.data:
            role = Role.query.get(data)
            user.roles.append(role)
        db.session.commit()
        flash(gettext('Roles updated successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/activate', methods=['POST'])
@roles_required('Admin')
def activate(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_activate_form = forms['user_activate_form']
    if user_activate_form.validate_on_submit():
        user.active = True
        user.fs_uniquifier = str(uuid.uuid4().hex)
        db.session.commit()
        flash(gettext('User activated successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/deactivate', methods=['POST'])
@roles_required('Admin')
def deactivate(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_deactivate_form = forms['user_deactivate_form']
    if user_deactivate_form.validate_on_submit():
        user.active = False
        user.fs_uniquifier = str(uuid.uuid4().hex)
        db.session.commit()
        flash(gettext('User deactivated successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/confirm', methods=['POST'])
@roles_required('Admin')
def confirm(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_confirm_form = forms['user_confirm_form']
    if user_confirm_form.validate_on_submit():
        user.confirmed_at = datetime.now()
        user.fs_uniquifier = str(uuid.uuid4().hex)
        db.session.commit()
        flash(gettext('User confirmed successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.detail', user_id=user_id))


@bp.route('/<int:user_id>/delete', methods=['POST'])
@roles_required('Admin')
def delete(user_id):
    user = User.query.get(user_id)
    forms = _initialize_forms(user)
    user_delete_form = forms['user_delete_form']
    if user_delete_form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        flash(gettext('User deleted successfully.'), 'success')
    else:
        return render_template('admin/users/detail.html', user=user, **forms)

    return redirect(url_for('users.index'))
