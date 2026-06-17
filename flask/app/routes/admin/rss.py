from flask import render_template, redirect, url_for, flash
from . import bp, admin_required
from ...extensions import db
from ...models.rss_item import RSSItem
from ...forms.admin_forms import RSSItemForm


@bp.route("/rss")
@admin_required
def rss_list():
    items = RSSItem.query.order_by(RSSItem.published_at.desc()).all()
    return render_template("admin/rss/list.html", items=items)


@bp.route("/rss/nouveau", methods=["GET", "POST"])
@admin_required
def rss_create():
    form = RSSItemForm()
    if form.validate_on_submit():
        item = RSSItem(
            title=form.title.data,
            link=form.link.data,
            description=form.description.data,
            category=form.category.data,
            is_active=form.is_active.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Élément RSS créé.", "success")
        return redirect(url_for("admin.rss_list"))
    return render_template("admin/rss/form.html", form=form, title="Nouvel élément RSS")


@bp.route("/rss/<int:rss_id>/supprimer", methods=["POST"])
@admin_required
def rss_delete(rss_id):
    item = RSSItem.query.get_or_404(rss_id)
    db.session.delete(item)
    db.session.commit()
    flash("Élément RSS supprimé.", "success")
    return redirect(url_for("admin.rss_list"))
