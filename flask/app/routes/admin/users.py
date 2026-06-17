from flask import render_template, redirect, url_for, flash, request
from . import bp, super_admin_required
from ...extensions import db
from ...models.user import User
from ...forms.admin_forms import UserForm


@bp.route("/utilisateurs")
@super_admin_required
def user_list():
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/users/list.html", users=users.items, pagination=users)


@bp.route("/utilisateurs/<int:user_id>/modifier", methods=["GET", "POST"])
@super_admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.role = form.role.data
        user.is_active = form.is_active.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("Utilisateur mis à jour.", "success")
        return redirect(url_for("admin.user_list"))
    return render_template("admin/users/form.html", form=form, user=user)
