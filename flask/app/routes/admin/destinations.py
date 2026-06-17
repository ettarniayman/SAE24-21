from flask import render_template, redirect, url_for, flash, request
from . import bp, admin_required, super_admin_required
from ...extensions import db
from ...models.destination import Destination
from ...models.country import Country
from ...forms.admin_forms import DestinationForm
from ...utils.helpers import save_uploaded_file
from slugify import slugify


@bp.route("/destinations")
@admin_required
def dest_list():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "")
    query = Destination.query
    if search:
        query = query.filter(Destination.name_fr.ilike(f"%{search}%"))
    pagination = query.order_by(Destination.name_fr).paginate(page=page, per_page=20)
    return render_template("admin/destinations/list.html", destinations=pagination.items, pagination=pagination, search=search)


@bp.route("/destinations/nouveau", methods=["GET", "POST"])
@admin_required
def dest_create():
    form = DestinationForm()
    form.country_id.choices = [(c.id, c.name_fr) for c in Country.query.order_by(Country.name_fr).all()]
    if form.validate_on_submit():
        dest = Destination()
        _fill_destination(dest, form)
        db.session.add(dest)
        db.session.commit()
        flash("Destination créée.", "success")
        return redirect(url_for("admin.dest_list"))
    return render_template("admin/destinations/form.html", form=form, title="Nouvelle destination")


@bp.route("/destinations/<int:dest_id>/modifier", methods=["GET", "POST"])
@admin_required
def dest_edit(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    form = DestinationForm(obj=dest)
    form.country_id.choices = [(c.id, c.name_fr) for c in Country.query.order_by(Country.name_fr).all()]
    if form.validate_on_submit():
        _fill_destination(dest, form)
        db.session.commit()
        flash("Destination mise à jour.", "success")
        return redirect(url_for("admin.dest_list"))
    return render_template("admin/destinations/form.html", form=form, dest=dest, title="Modifier la destination")


@bp.route("/destinations/<int:dest_id>/supprimer", methods=["POST"])
@super_admin_required
def dest_delete(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    db.session.delete(dest)
    db.session.commit()
    flash("Destination supprimée.", "success")
    return redirect(url_for("admin.dest_list"))


def _fill_destination(dest, form):
    dest.name_fr = form.name_fr.data
    dest.name_en = form.name_en.data
    dest.slug = form.slug.data or slugify(form.name_fr.data)
    dest.country_id = form.country_id.data
    dest.region = form.region.data
    dest.short_desc_fr = form.short_desc_fr.data
    dest.short_desc_en = form.short_desc_en.data
    dest.long_desc_fr = form.long_desc_fr.data
    dest.long_desc_en = form.long_desc_en.data
    dest.history_fr = form.history_fr.data
    dest.culture_fr = form.culture_fr.data
    dest.gastronomy_fr = form.gastronomy_fr.data
    dest.latitude = form.latitude.data
    dest.longitude = form.longitude.data
    dest.average_budget_eur = form.average_budget_eur.data
    dest.difficulty_level = form.difficulty_level.data
    dest.safety_level = form.safety_level.data
    dest.best_period_fr = form.best_period_fr.data
    dest.climate_fr = form.climate_fr.data
    dest.destination_type = form.destination_type.data
    dest.is_featured = form.is_featured.data
    dest.is_active = form.is_active.data
    dest.video_url = form.video_url.data
    dest.youtube_id = form.youtube_id.data
    dest.street_view_lat = form.street_view_lat.data
    dest.street_view_lng = form.street_view_lng.data
    dest.meta_title_fr = form.meta_title_fr.data
    dest.meta_desc_fr = form.meta_desc_fr.data
    if form.image_main.data and hasattr(form.image_main.data, "filename"):
        filename = save_uploaded_file(form.image_main.data, "destinations")
        if filename:
            dest.image_main = filename
