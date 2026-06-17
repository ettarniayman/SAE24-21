from flask import render_template, redirect, url_for, flash
from . import bp, admin_required, super_admin_required
from ...extensions import db
from ...models.country import Country
from ...forms.admin_forms import CountryForm


@bp.route("/pays")
@admin_required
def country_list():
    countries = Country.query.order_by(Country.continent, Country.name_fr).all()
    return render_template("admin/countries/list.html", countries=countries)


@bp.route("/pays/nouveau", methods=["GET", "POST"])
@admin_required
def country_create():
    form = CountryForm()
    if form.validate_on_submit():
        country = Country()
        _fill_country(country, form)
        db.session.add(country)
        db.session.commit()
        flash("Pays créé.", "success")
        return redirect(url_for("admin.country_list"))
    return render_template("admin/countries/form.html", form=form, title="Nouveau pays")


@bp.route("/pays/<int:country_id>/modifier", methods=["GET", "POST"])
@admin_required
def country_edit(country_id):
    country = Country.query.get_or_404(country_id)
    form = CountryForm(obj=country)
    if form.validate_on_submit():
        _fill_country(country, form)
        db.session.commit()
        flash("Pays mis à jour.", "success")
        return redirect(url_for("admin.country_list"))
    return render_template("admin/countries/form.html", form=form, country=country, title="Modifier le pays")


@bp.route("/pays/<int:country_id>/supprimer", methods=["POST"])
@super_admin_required
def country_delete(country_id):
    country = Country.query.get_or_404(country_id)
    db.session.delete(country)
    db.session.commit()
    flash("Pays supprimé.", "success")
    return redirect(url_for("admin.country_list"))


def _fill_country(country, form):
    country.name_fr = form.name_fr.data
    country.name_en = form.name_en.data
    country.code = form.code.data
    country.continent = form.continent.data
    country.capital = form.capital.data
    country.currency = form.currency.data
    country.flag_emoji = form.flag_emoji.data
    country.is_active = form.is_active.data
