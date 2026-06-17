from flask import render_template, redirect, url_for, flash
from . import bp, admin_required
from ...extensions import db
from ...models.faq import FAQCategory, FAQItem
from ...forms.admin_forms import FAQForm


@bp.route("/faq")
@admin_required
def faq_list():
    categories = FAQCategory.query.order_by(FAQCategory.order).all()
    return render_template("admin/faq/list.html", categories=categories)


@bp.route("/faq/item/nouveau", methods=["GET", "POST"])
@admin_required
def faq_create():
    form = FAQForm()
    form.category_id.choices = [(c.id, c.name_fr) for c in FAQCategory.query.all()]
    if form.validate_on_submit():
        item = FAQItem(
            category_id=form.category_id.data,
            question_fr=form.question_fr.data,
            answer_fr=form.answer_fr.data,
            is_active=form.is_active.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Question FAQ créée.", "success")
        return redirect(url_for("admin.faq_list"))
    return render_template("admin/faq/form.html", form=form, title="Nouvelle question")


@bp.route("/faq/item/<int:item_id>/modifier", methods=["GET", "POST"])
@admin_required
def faq_edit(item_id):
    item = FAQItem.query.get_or_404(item_id)
    form = FAQForm(obj=item)
    form.category_id.choices = [(c.id, c.name_fr) for c in FAQCategory.query.all()]
    if form.validate_on_submit():
        item.category_id = form.category_id.data
        item.question_fr = form.question_fr.data
        item.answer_fr = form.answer_fr.data
        item.is_active = form.is_active.data
        db.session.commit()
        flash("Question FAQ mise à jour.", "success")
        return redirect(url_for("admin.faq_list"))
    return render_template("admin/faq/form.html", form=form, item=item, title="Modifier la question")


@bp.route("/faq/item/<int:item_id>/supprimer", methods=["POST"])
@admin_required
def faq_delete(item_id):
    item = FAQItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Question supprimée.", "success")
    return redirect(url_for("admin.faq_list"))
