from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User
from ..models.booking import Booking
from ..forms.auth_forms import LoginForm, RegisterForm, ProfileForm
from ..extensions import db
from datetime import datetime, timezone

bp = Blueprint("auth", __name__)


@bp.route("/connexion", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.email == form.identifier.data.lower()) | (User.username == form.identifier.data)
        ).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            if user.is_admin():
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("main.index"))
        flash("Identifiants incorrects.", "danger")
    return render_template("auth/login.html", form=form)


@bp.route("/inscription", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter(
            (User.email == form.email.data.lower()) | (User.username == form.username.data)
        ).first()
        if existing:
            flash("Email ou nom d'utilisateur déjà utilisé.", "danger")
        else:
            user = User(
                username=form.username.data,
                email=form.email.data.lower(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data or None,
                role="client",
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Compte créé avec succès !", "success")
            return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=form)


@bp.route("/deconnexion")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/profil", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data.lower()
        current_user.phone = form.phone.data or None
        db.session.commit()
        flash("Profil mis à jour.", "success")
        return redirect(url_for("auth.profile"))
    bookings = current_user.bookings.order_by(Booking.created_at.desc()).limit(10).all()
    return render_template("auth/profile.html", form=form, bookings=bookings)
