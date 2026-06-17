from flask import render_template, redirect, url_for, flash, request
from . import bp, admin_required, super_admin_required
from ...extensions import db
from ...models.program import TravelProgram
from ...forms.admin_forms import ProgramForm
from slugify import slugify


@bp.route("/programmes")
@admin_required
def program_list():
    page = request.args.get("page", 1, type=int)
    programs = TravelProgram.query.order_by(TravelProgram.name_fr).paginate(page=page, per_page=20)
    return render_template("admin/programs/list.html", programs=programs.items, pagination=programs)


@bp.route("/programmes/nouveau", methods=["GET", "POST"])
@admin_required
def program_create():
    form = ProgramForm()
    if form.validate_on_submit():
        prog = TravelProgram()
        _fill_program(prog, form)
        db.session.add(prog)
        db.session.commit()
        flash("Programme créé.", "success")
        return redirect(url_for("admin.program_list"))
    return render_template("admin/programs/form.html", form=form, title="Nouveau programme")


@bp.route("/programmes/<int:prog_id>/modifier", methods=["GET", "POST"])
@admin_required
def program_edit(prog_id):
    prog = TravelProgram.query.get_or_404(prog_id)
    form = ProgramForm(obj=prog)
    if form.validate_on_submit():
        _fill_program(prog, form)
        db.session.commit()
        flash("Programme mis à jour.", "success")
        return redirect(url_for("admin.program_list"))
    return render_template("admin/programs/form.html", form=form, prog=prog, title="Modifier le programme")


@bp.route("/programmes/<int:prog_id>/supprimer", methods=["POST"])
@super_admin_required
def program_delete(prog_id):
    prog = TravelProgram.query.get_or_404(prog_id)
    db.session.delete(prog)
    db.session.commit()
    flash("Programme supprimé.", "success")
    return redirect(url_for("admin.program_list"))


def _fill_program(prog, form):
    prog.name_fr = form.name_fr.data
    prog.name_en = form.name_en.data
    prog.slug = form.slug.data or slugify(form.name_fr.data)
    prog.description_fr = form.description_fr.data
    prog.duration_days = form.duration_days.data
    prog.price_per_person = form.price_per_person.data
    prog.price_per_person_discounted = form.price_per_person_discounted.data
    prog.theme = form.theme.data
    prog.difficulty = form.difficulty.data
    prog.includes_fr = form.includes_fr.data
    prog.excludes_fr = form.excludes_fr.data
    prog.departure_city = form.departure_city.data
    prog.is_featured = form.is_featured.data
    prog.is_active = form.is_active.data
