from flask import render_template, redirect, url_for, flash, request
from . import bp, admin_required, super_admin_required
from ...extensions import db
from ...models.shop import ShopProduct, ShopCategory
from ...forms.admin_forms import ShopProductForm, ShopCategoryForm
from slugify import slugify


# ─── Catégories ───────────────────────────────────────────────────────────────

@bp.route("/boutique/categories")
@admin_required
def shop_category_list():
    categories = ShopCategory.query.order_by(ShopCategory.name_fr).all()
    return render_template("admin/shop/category_list.html", categories=categories)


@bp.route("/boutique/categories/nouvelle", methods=["GET", "POST"])
@admin_required
def shop_category_create():
    form = ShopCategoryForm()
    if form.validate_on_submit():
        category = ShopCategory()
        _fill_shop_category(category, form)
        db.session.add(category)
        db.session.commit()
        flash("Catégorie créée.", "success")
        return redirect(url_for("admin.shop_category_list"))
    return render_template("admin/shop/category_form.html", form=form, title="Nouvelle catégorie")


@bp.route("/boutique/categories/<int:category_id>/modifier", methods=["GET", "POST"])
@admin_required
def shop_category_edit(category_id):
    category = ShopCategory.query.get_or_404(category_id)
    form = ShopCategoryForm(obj=category)
    if form.validate_on_submit():
        _fill_shop_category(category, form)
        db.session.commit()
        flash("Catégorie mise à jour.", "success")
        return redirect(url_for("admin.shop_category_list"))
    return render_template("admin/shop/category_form.html", form=form, category=category, title="Modifier la catégorie")


@bp.route("/boutique/categories/<int:category_id>/supprimer", methods=["POST"])
@super_admin_required
def shop_category_delete(category_id):
    category = ShopCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Catégorie supprimée.", "success")
    return redirect(url_for("admin.shop_category_list"))


def _fill_shop_category(category, form):
    category.name_fr = form.name_fr.data
    category.name_en = form.name_en.data
    category.slug = form.slug.data or slugify(form.name_fr.data)
    category.icon = form.icon.data
    category.is_active = form.is_active.data


# ─── Produits ─────────────────────────────────────────────────────────────────

@bp.route("/boutique")
@admin_required
def shop_list():
    page = request.args.get("page", 1, type=int)
    products = ShopProduct.query.order_by(ShopProduct.name_fr).paginate(page=page, per_page=20)
    return render_template("admin/shop/list.html", products=products.items, pagination=products)


@bp.route("/boutique/nouveau", methods=["GET", "POST"])
@admin_required
def shop_create():
    form = ShopProductForm()
    form.category_id.choices = [(0, "— Aucune —")] + [
        (c.id, c.name_fr) for c in ShopCategory.query.order_by(ShopCategory.name_fr).all()
    ]
    if form.validate_on_submit():
        product = ShopProduct()
        _fill_shop_product(product, form)
        db.session.add(product)
        db.session.commit()
        flash("Produit créé.", "success")
        return redirect(url_for("admin.shop_list"))
    return render_template("admin/shop/form.html", form=form, title="Nouveau produit")


@bp.route("/boutique/<int:product_id>/modifier", methods=["GET", "POST"])
@admin_required
def shop_edit(product_id):
    product = ShopProduct.query.get_or_404(product_id)
    form = ShopProductForm(obj=product)
    form.category_id.choices = [(0, "— Aucune —")] + [
        (c.id, c.name_fr) for c in ShopCategory.query.order_by(ShopCategory.name_fr).all()
    ]
    if form.validate_on_submit():
        _fill_shop_product(product, form)
        db.session.commit()
        flash("Produit mis à jour.", "success")
        return redirect(url_for("admin.shop_list"))
    return render_template("admin/shop/form.html", form=form, product=product, title="Modifier le produit")


@bp.route("/boutique/<int:product_id>/supprimer", methods=["POST"])
@super_admin_required
def shop_delete(product_id):
    product = ShopProduct.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Produit supprimé.", "success")
    return redirect(url_for("admin.shop_list"))


def _fill_shop_product(product, form):
    product.name_fr = form.name_fr.data
    product.name_en = form.name_en.data
    product.slug = form.slug.data or slugify(form.name_fr.data)
    category_id = form.category_id.data
    product.category_id = category_id if category_id else None
    product.description_fr = form.description_fr.data
    product.price = form.price.data
    product.price_discounted = form.price_discounted.data
    product.stock = form.stock.data
    product.affiliate_url = form.affiliate_url.data
    product.is_affiliate = form.is_affiliate.data
    product.is_featured = form.is_featured.data
    product.is_active = form.is_active.data
