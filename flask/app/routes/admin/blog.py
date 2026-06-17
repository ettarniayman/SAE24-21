from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from . import bp, admin_required, super_admin_required
from ...extensions import db
from ...models.blog import BlogPost, BlogCategory
from ...forms.admin_forms import BlogPostForm
from slugify import slugify


@bp.route("/blog")
@admin_required
def blog_list():
    page = request.args.get("page", 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/blog/list.html", posts=posts.items, pagination=posts)


@bp.route("/blog/nouveau", methods=["GET", "POST"])
@admin_required
def blog_create():
    form = BlogPostForm()
    form.category_id.choices = [(c.id, c.name_fr) for c in BlogCategory.query.all()]
    if form.validate_on_submit():
        post = BlogPost(author_id=current_user.id)
        _fill_blog_post(post, form)
        if form.is_published.data:
            post.publish()
        db.session.add(post)
        db.session.commit()
        flash("Article créé.", "success")
        return redirect(url_for("admin.blog_list"))
    return render_template("admin/blog/form.html", form=form, title="Nouvel article")


@bp.route("/blog/<int:post_id>/modifier", methods=["GET", "POST"])
@admin_required
def blog_edit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)
    form.category_id.choices = [(c.id, c.name_fr) for c in BlogCategory.query.all()]
    if form.validate_on_submit():
        _fill_blog_post(post, form)
        if form.is_published.data and not post.is_published:
            post.publish()
        db.session.commit()
        flash("Article mis à jour.", "success")
        return redirect(url_for("admin.blog_list"))
    return render_template("admin/blog/form.html", form=form, post=post, title="Modifier l'article")


@bp.route("/blog/<int:post_id>/supprimer", methods=["POST"])
@super_admin_required
def blog_delete(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Article supprimé.", "success")
    return redirect(url_for("admin.blog_list"))


def _fill_blog_post(post, form):
    post.title_fr = form.title_fr.data
    post.title_en = form.title_en.data
    post.slug = form.slug.data or slugify(form.title_fr.data)
    post.excerpt_fr = form.excerpt_fr.data
    post.content_fr = form.content_fr.data
    post.content_en = form.content_en.data
    post.category_id = form.category_id.data
    post.is_featured = form.is_featured.data
    post.is_published = form.is_published.data
    post.meta_title_fr = form.meta_title_fr.data
    post.meta_desc_fr = form.meta_desc_fr.data
