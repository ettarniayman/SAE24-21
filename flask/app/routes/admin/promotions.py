from flask import render_template, redirect, url_for, flash
from . import bp, admin_required
from ...extensions import db
from ...models.promotion import Promotion
from ...models.destination import Destination
from ...forms.admin_forms import PromotionForm
from slugify import slugify


@bp.route("/promotions")
@admin_required
def promotion_list():
    promos = Promotion.query.order_by(Promotion.created_at.desc()).all()
    return render_template("admin/promotions/list.html", promos=promos)


@bp.route("/promotions/nouvelle", methods=["GET", "POST"])
@admin_required
def promotion_create():
    form = PromotionForm()
    form.destination_id.choices = [(0, "— Aucune —")] + [
        (d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()
    ]
    if form.validate_on_submit():
        promo = Promotion()
        _fill_promotion(promo, form)
        db.session.add(promo)
        db.session.commit()
        flash("Promotion créée.", "success")
        return redirect(url_for("admin.promotion_list"))
    return render_template("admin/promotions/form.html", form=form, title="Nouvelle promotion")


@bp.route("/promotions/<int:promo_id>/modifier", methods=["GET", "POST"])
@admin_required
def promotion_edit(promo_id):
    promo = Promotion.query.get_or_404(promo_id)
    form = PromotionForm(obj=promo)
    form.destination_id.choices = [(0, "— Aucune —")] + [
        (d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()
    ]
    if form.validate_on_submit():
        _fill_promotion(promo, form)
        db.session.commit()
        flash("Promotion mise à jour.", "success")
        return redirect(url_for("admin.promotion_list"))
    return render_template("admin/promotions/form.html", form=form, promo=promo, title="Modifier la promotion")


@bp.route("/promotions/<int:promo_id>/supprimer", methods=["POST"])
@admin_required
def promotion_delete(promo_id):
    promo = Promotion.query.get_or_404(promo_id)
    db.session.delete(promo)
    db.session.commit()
    flash("Promotion supprimée.", "success")
    return redirect(url_for("admin.promotion_list"))


def _fill_promotion(promo, form):
    promo.title_fr = form.title_fr.data
    promo.title_en = form.title_en.data
    promo.slug = form.slug.data or slugify(form.title_fr.data)
    promo.description_fr = form.description_fr.data
    promo.original_price = form.original_price.data
    promo.promo_price = form.promo_price.data
    promo.discount_percent = form.discount_percent.data
    promo.promo_code = form.promo_code.data
    promo.valid_from = form.valid_from.data
    promo.valid_until = form.valid_until.data
    promo.is_active = form.is_active.data
    promo.is_featured = form.is_featured.data
    promo.promo_type = form.promo_type.data
    dest_id = form.destination_id.data
    promo.destination_id = dest_id if dest_id else None
