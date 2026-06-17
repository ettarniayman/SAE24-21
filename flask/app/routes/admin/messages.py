from flask import render_template, redirect, url_for, flash, request
from . import bp, admin_required
from ...extensions import db
from ...models.contact import ContactMessage


@bp.route("/messages")
@admin_required
def message_list():
    page = request.args.get("page", 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/messages/list.html", messages=messages.items, pagination=messages)


@bp.route("/messages/<int:msg_id>")
@admin_required
def message_detail(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    if not msg.is_read:
        msg.is_read = True
        db.session.commit()
    return render_template("admin/messages/detail.html", msg=msg)


@bp.route("/messages/<int:msg_id>/supprimer", methods=["POST"])
@admin_required
def message_delete(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message supprimé.", "success")
    return redirect(url_for("admin.message_list"))
