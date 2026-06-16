from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.contact import ContactMessage
from ..forms.contact_forms import ContactForm
from ..extensions import db

bp = Blueprint("contact", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = ContactForm()
    success = False
    if form.validate_on_submit():
        msg = ContactMessage(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip() if form.phone.data else None,
            destination_interest=form.destination_interest.data,
            subject=form.subject.data.strip(),
            message=form.message.data.strip(),
            ip_address=request.remote_addr,
        )
        db.session.add(msg)
        db.session.commit()
        success = True
    return render_template("pages/contact.html", form=form, success=success)
