from flask import Blueprint, render_template, request
from ..models.blog import BlogPost, BlogCategory, BlogTag
from ..extensions import db

bp = Blueprint("blog", __name__)


@bp.route("/")
def list_posts():
    page = request.args.get("page", 1, type=int)
    category_slug = request.args.get("cat", "")
    tag_slug = request.args.get("tag", "")
    search = request.args.get("q", "")

    query = BlogPost.query.filter_by(is_published=True)

    if category_slug:
        cat = BlogCategory.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    if tag_slug:
        tag = BlogTag.query.filter_by(slug=tag_slug).first()
        if tag:
            query = query.filter(BlogPost.tags.any(id=tag.id))

    if search:
        query = query.filter(
            db.or_(BlogPost.title_fr.ilike(f"%{search}%"), BlogPost.excerpt_fr.ilike(f"%{search}%"))
        )

    query = query.order_by(BlogPost.published_at.desc())
    pagination = query.paginate(page=page, per_page=9, error_out=False)
    categories = BlogCategory.query.filter_by(is_active=True).all()
    recent = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).limit(5).all()

    return render_template(
        "blog/list.html",
        posts=pagination.items,
        pagination=pagination,
        categories=categories,
        recent=recent,
        current_cat=category_slug,
        search=search,
    )


@bp.route("/<slug>")
def post_detail(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    post.view_count = (post.view_count or 0) + 1
    db.session.commit()
    related = (
        BlogPost.query
        .filter(BlogPost.category_id == post.category_id, BlogPost.id != post.id, BlogPost.is_published == True)
        .order_by(BlogPost.published_at.desc()).limit(3).all()
    )
    categories = BlogCategory.query.filter_by(is_active=True).all()
    return render_template("blog/detail.html", post=post, related=related, categories=categories)
