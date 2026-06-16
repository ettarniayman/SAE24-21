from flask import Blueprint, render_template, request
from ..models.shop import ShopProduct, ShopCategory

bp = Blueprint("shop", __name__)


@bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    cat_slug = request.args.get("cat", "")
    sort = request.args.get("sort", "featured")

    query = ShopProduct.query.filter_by(is_active=True)
    if cat_slug:
        cat = ShopCategory.query.filter_by(slug=cat_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    if sort == "price_asc":
        query = query.order_by(ShopProduct.price.asc())
    elif sort == "price_desc":
        query = query.order_by(ShopProduct.price.desc())
    else:
        query = query.order_by(ShopProduct.is_featured.desc(), ShopProduct.rating.desc())

    pagination = query.paginate(page=page, per_page=12, error_out=False)
    categories = ShopCategory.query.filter_by(is_active=True).all()

    return render_template(
        "shop/index.html",
        products=pagination.items,
        pagination=pagination,
        categories=categories,
        current_cat=cat_slug,
        current_sort=sort,
    )


@bp.route("/<slug>")
def product_detail(slug):
    product = ShopProduct.query.filter_by(slug=slug, is_active=True).first_or_404()
    related = ShopProduct.query.filter(
        ShopProduct.category_id == product.category_id,
        ShopProduct.id != product.id,
        ShopProduct.is_active == True,
    ).limit(4).all()
    return render_template("shop/product.html", product=product, related=related)
