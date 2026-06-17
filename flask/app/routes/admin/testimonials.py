from flask import render_template, redirect, url_for, flash
from . import bp, admin_required
from ...extensions import db
from ...models.testimonial import Testimonial


@bp.route("/temoignages")
@admin_required
def testimonial_list():
    pending = Testimonial.query.filter_by(is_approved=False).all()
    approved = Testimonial.query.filter_by(is_approved=True).order_by(Testimonial.created_at.desc()).limit(30).all()
    return render_template("admin/testimonials/list.html", pending=pending, approved=approved)


@bp.route("/temoignages/<int:t_id>/approuver", methods=["POST"])
@admin_required
def testimonial_approve(t_id):
    t = Testimonial.query.get_or_404(t_id)
    t.is_approved = True
    db.session.commit()
    flash("Témoignage approuvé.", "success")
    return redirect(url_for("admin.testimonial_list"))


@bp.route("/temoignages/<int:t_id>/supprimer", methods=["POST"])
@admin_required
def testimonial_delete(t_id):
    t = Testimonial.query.get_or_404(t_id)
    db.session.delete(t)
    db.session.commit()
    flash("Témoignage supprimé.", "success")
    return redirect(url_for("admin.testimonial_list"))
