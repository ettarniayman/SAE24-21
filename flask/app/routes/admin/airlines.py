from flask import render_template, redirect, url_for, flash
from . import bp, admin_required, super_admin_required
from ...extensions import db
from ...models.airline import Airline
from ...forms.admin_forms import AirlineForm
from slugify import slugify


@bp.route("/compagnies")
@admin_required
def airline_list():
    airlines = Airline.query.order_by(Airline.name).all()
    return render_template("admin/airlines/list.html", airlines=airlines)


@bp.route("/compagnies/nouvelle", methods=["GET", "POST"])
@admin_required
def airline_create():
    form = AirlineForm()
    if form.validate_on_submit():
        airline = Airline()
        _fill_airline(airline, form)
        db.session.add(airline)
        db.session.commit()
        flash("Compagnie aérienne créée.", "success")
        return redirect(url_for("admin.airline_list"))
    return render_template("admin/airlines/form.html", form=form, title="Nouvelle compagnie aérienne")


@bp.route("/compagnies/<int:airline_id>/modifier", methods=["GET", "POST"])
@admin_required
def airline_edit(airline_id):
    airline = Airline.query.get_or_404(airline_id)
    form = AirlineForm(obj=airline)
    if form.validate_on_submit():
        _fill_airline(airline, form)
        db.session.commit()
        flash("Compagnie aérienne mise à jour.", "success")
        return redirect(url_for("admin.airline_list"))
    return render_template("admin/airlines/form.html", form=form, airline=airline, title="Modifier la compagnie aérienne")


@bp.route("/compagnies/<int:airline_id>/supprimer", methods=["POST"])
@super_admin_required
def airline_delete(airline_id):
    airline = Airline.query.get_or_404(airline_id)
    db.session.delete(airline)
    db.session.commit()
    flash("Compagnie aérienne supprimée.", "success")
    return redirect(url_for("admin.airline_list"))


def _fill_airline(airline, form):
    airline.name = form.name.data
    airline.slug = form.slug.data or slugify(form.name.data)
    airline.iata_code = form.iata_code.data
    airline.website = form.website.data
    airline.description_fr = form.description_fr.data
    airline.is_partner = form.is_partner.data
    airline.is_active = form.is_active.data
