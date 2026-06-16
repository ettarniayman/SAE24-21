from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
from ...extensions import db
from ...models.destination import Destination
from ...models.country import Country
from ...models.activity import Activity, ActivityCategory
from ...models.hotel import Hotel
from ...models.program import TravelProgram, ProgramDay
from ...models.airline import Airline, FlightPromotion
from ...models.testimonial import Testimonial
from ...models.blog import BlogPost, BlogCategory, BlogTag
from ...models.contact import ContactMessage
from ...models.newsletter import NewsletterSubscriber
from ...models.faq import FAQCategory, FAQItem
from ...models.promotion import Promotion
from ...models.media import Media
from ...models.shop import ShopProduct, ShopCategory
from ...models.booking import Booking
from ...models.user import User
from ...models.rss_item import RSSItem
from ...forms.admin_forms import (
    DestinationForm, HotelForm, ProgramForm, BlogPostForm,
    AirlineForm, PromotionForm, FAQForm, TestimonialForm,
    UserForm, ShopProductForm, RSSItemForm, CountryForm,
    ActivityForm,
)
from ...utils.helpers import save_uploaded_file
from python_slugify import slugify
import os

bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_agent():
            flash("Accès refusé.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated


def super_admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin():
            flash("Accès réservé aux administrateurs.", "danger")
            return redirect(url_for("admin.dashboard"))
        return f(*args, **kwargs)
    return decorated


# ─── Dashboard ───────────────────────────────────────────────────────────────

@bp.route("/")
@admin_required
def dashboard():
    stats = {
        "destinations": Destination.query.count(),
        "programs": TravelProgram.query.count(),
        "hotels": Hotel.query.count(),
        "bookings": Booking.query.count(),
        "users": User.query.count(),
        "messages": ContactMessage.query.filter_by(is_read=False).count(),
        "testimonials_pending": Testimonial.query.filter_by(is_approved=False).count(),
        "newsletter": NewsletterSubscriber.query.filter_by(is_active=True).count(),
    }
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    pending_testimonials = Testimonial.query.filter_by(is_approved=False).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_bookings=recent_bookings,
        recent_messages=recent_messages,
        pending_testimonials=pending_testimonials,
    )


# ─── Destinations ─────────────────────────────────────────────────────────────

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


# ─── Hotels ───────────────────────────────────────────────────────────────────

@bp.route("/hotels")
@admin_required
def hotel_list():
    page = request.args.get("page", 1, type=int)
    hotels = Hotel.query.order_by(Hotel.name).paginate(page=page, per_page=20)
    return render_template("admin/hotels/list.html", hotels=hotels.items, pagination=hotels)


@bp.route("/hotels/nouveau", methods=["GET", "POST"])
@admin_required
def hotel_create():
    form = HotelForm()
    form.destination_id.choices = [(d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()]
    if form.validate_on_submit():
        hotel = Hotel()
        _fill_hotel(hotel, form)
        db.session.add(hotel)
        db.session.commit()
        flash("Hôtel créé.", "success")
        return redirect(url_for("admin.hotel_list"))
    return render_template("admin/hotels/form.html", form=form, title="Nouvel hôtel")


@bp.route("/hotels/<int:hotel_id>/modifier", methods=["GET", "POST"])
@admin_required
def hotel_edit(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    form = HotelForm(obj=hotel)
    form.destination_id.choices = [(d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()]
    if form.validate_on_submit():
        _fill_hotel(hotel, form)
        db.session.commit()
        flash("Hôtel mis à jour.", "success")
        return redirect(url_for("admin.hotel_list"))
    return render_template("admin/hotels/form.html", form=form, hotel=hotel, title="Modifier l'hôtel")


@bp.route("/hotels/<int:hotel_id>/supprimer", methods=["POST"])
@super_admin_required
def hotel_delete(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    flash("Hôtel supprimé.", "success")
    return redirect(url_for("admin.hotel_list"))


def _fill_hotel(hotel, form):
    hotel.name = form.name.data
    hotel.slug = form.slug.data or slugify(form.name.data)
    hotel.destination_id = form.destination_id.data
    hotel.hotel_type = form.hotel_type.data
    hotel.stars = form.stars.data
    hotel.address = form.address.data
    hotel.latitude = form.latitude.data
    hotel.longitude = form.longitude.data
    hotel.description_fr = form.description_fr.data
    hotel.price_min = form.price_min.data
    hotel.price_max = form.price_max.data
    hotel.has_pool = form.has_pool.data
    hotel.has_spa = form.has_spa.data
    hotel.has_restaurant = form.has_restaurant.data
    hotel.has_wifi = form.has_wifi.data
    hotel.booking_url = form.booking_url.data
    hotel.is_partner = form.is_partner.data
    hotel.is_featured = form.is_featured.data
    hotel.is_active = form.is_active.data


# ─── Programmes ───────────────────────────────────────────────────────────────

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


# ─── Blog ─────────────────────────────────────────────────────────────────────

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


# ─── Utilisateurs ────────────────────────────────────────────────────────────

@bp.route("/utilisateurs")
@super_admin_required
def user_list():
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/users/list.html", users=users.items, pagination=users)


@bp.route("/utilisateurs/<int:user_id>/modifier", methods=["GET", "POST"])
@super_admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.role = form.role.data
        user.is_active = form.is_active.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("Utilisateur mis à jour.", "success")
        return redirect(url_for("admin.user_list"))
    return render_template("admin/users/form.html", form=form, user=user)


# ─── Témoignages ──────────────────────────────────────────────────────────────

@bp.route("/temoignages")
@admin_required
def testimonial_list():
    pending = Testimonial.query.filter_by(is_approved=False).all()
    approved = Testimonial.query.filter_by(is_approved=True).order_by(Testimonial.created_at.desc()).limit(30).all()
    return render_template("admin/testimonials/list.html", pending=pending, approved=approved)


@bp.route("/temoignages/<int:t_id>/approuver", methods=["POST"])
@admin_required
def testimonial_approve(t_id):
    t = Testimonial.query.get_or_404(t_id)
    t.is_approved = True
    db.session.commit()
    flash("Témoignage approuvé.", "success")
    return redirect(url_for("admin.testimonial_list"))


@bp.route("/temoignages/<int:t_id>/supprimer", methods=["POST"])
@admin_required
def testimonial_delete(t_id):
    t = Testimonial.query.get_or_404(t_id)
    db.session.delete(t)
    db.session.commit()
    flash("Témoignage supprimé.", "success")
    return redirect(url_for("admin.testimonial_list"))


# ─── Promotions ───────────────────────────────────────────────────────────────

@bp.route("/promotions")
@admin_required
def promotion_list():
    promos = Promotion.query.order_by(Promotion.created_at.desc()).all()
    return render_template("admin/promotions/list.html", promos=promos)


@bp.route("/promotions/nouvelle", methods=["GET", "POST"])
@admin_required
def promotion_create():
    form = PromotionForm()
    form.destination_id.choices = [(0, "— Aucune —")] + [
        (d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()
    ]
    if form.validate_on_submit():
        promo = Promotion()
        _fill_promotion(promo, form)
        db.session.add(promo)
        db.session.commit()
        flash("Promotion créée.", "success")
        return redirect(url_for("admin.promotion_list"))
    return render_template("admin/promotions/form.html", form=form, title="Nouvelle promotion")


@bp.route("/promotions/<int:promo_id>/modifier", methods=["GET", "POST"])
@admin_required
def promotion_edit(promo_id):
    promo = Promotion.query.get_or_404(promo_id)
    form = PromotionForm(obj=promo)
    form.destination_id.choices = [(0, "— Aucune —")] + [
        (d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()
    ]
    if form.validate_on_submit():
        _fill_promotion(promo, form)
        db.session.commit()
        flash("Promotion mise à jour.", "success")
        return redirect(url_for("admin.promotion_list"))
    return render_template("admin/promotions/form.html", form=form, promo=promo, title="Modifier la promotion")


@bp.route("/promotions/<int:promo_id>/supprimer", methods=["POST"])
@admin_required
def promotion_delete(promo_id):
    promo = Promotion.query.get_or_404(promo_id)
    db.session.delete(promo)
    db.session.commit()
    flash("Promotion supprimée.", "success")
    return redirect(url_for("admin.promotion_list"))


def _fill_promotion(promo, form):
    promo.title_fr = form.title_fr.data
    promo.title_en = form.title_en.data
    promo.slug = form.slug.data or slugify(form.title_fr.data)
    promo.description_fr = form.description_fr.data
    promo.original_price = form.original_price.data
    promo.promo_price = form.promo_price.data
    promo.discount_percent = form.discount_percent.data
    promo.promo_code = form.promo_code.data
    promo.valid_from = form.valid_from.data
    promo.valid_until = form.valid_until.data
    promo.is_active = form.is_active.data
    promo.is_featured = form.is_featured.data
    promo.promo_type = form.promo_type.data
    dest_id = form.destination_id.data
    promo.destination_id = dest_id if dest_id else None


# ─── Messages ─────────────────────────────────────────────────────────────────

@bp.route("/messages")
@admin_required
def message_list():
    page = request.args.get("page", 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/messages/list.html", messages=messages.items, pagination=messages)


@bp.route("/messages/<int:msg_id>")
@admin_required
def message_detail(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    if not msg.is_read:
        msg.is_read = True
        db.session.commit()
    return render_template("admin/messages/detail.html", msg=msg)


@bp.route("/messages/<int:msg_id>/supprimer", methods=["POST"])
@admin_required
def message_delete(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message supprimé.", "success")
    return redirect(url_for("admin.message_list"))


# ─── FAQ ──────────────────────────────────────────────────────────────────────

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


# ─── RSS ──────────────────────────────────────────────────────────────────────

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


# ─── Médias ───────────────────────────────────────────────────────────────────

@bp.route("/medias")
@admin_required
def media_list():
    page = request.args.get("page", 1, type=int)
    medias = Media.query.order_by(Media.created_at.desc()).paginate(page=page, per_page=24)
    return render_template("admin/media/list.html", medias=medias.items, pagination=medias)


@bp.route("/medias/upload", methods=["POST"])
@admin_required
def media_upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file"}), 400
    filename = save_uploaded_file(file, "uploads")
    if not filename:
        return jsonify({"error": "Invalid file type"}), 400
    dest_id = request.form.get("destination_id", type=int)
    media = Media(
        filename=filename,
        original_name=file.filename,
        file_path=f"/static/images/uploads/{filename}",
        file_type="image",
        destination_id=dest_id,
        uploaded_by=current_user.id,
    )
    db.session.add(media)
    db.session.commit()
    return jsonify({"success": True, "path": media.file_path, "id": media.id})


@bp.route("/medias/<int:media_id>/supprimer", methods=["POST"])
@admin_required
def media_delete(media_id):
    media = Media.query.get_or_404(media_id)
    full_path = os.path.join(current_app.root_path, "static", "images", "uploads", media.filename)
    if os.path.exists(full_path):
        os.remove(full_path)
    db.session.delete(media)
    db.session.commit()
    flash("Média supprimé.", "success")
    return redirect(url_for("admin.media_list"))


# ─── Newsletter ───────────────────────────────────────────────────────────────

@bp.route("/newsletter")
@admin_required
def newsletter_list():
    page = request.args.get("page", 1, type=int)
    subs = NewsletterSubscriber.query.filter_by(is_active=True).order_by(
        NewsletterSubscriber.subscribed_at.desc()
    ).paginate(page=page, per_page=30)
    total = NewsletterSubscriber.query.filter_by(is_active=True).count()
    return render_template("admin/newsletter/list.html", subs=subs.items, pagination=subs, total=total)


# ─── Réservations ─────────────────────────────────────────────────────────────

@bp.route("/reservations")
@admin_required
def booking_list():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status", "")
    query = Booking.query
    if status:
        query = query.filter_by(status=status)
    bookings = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/bookings/list.html", bookings=bookings.items, pagination=bookings, current_status=status)


@bp.route("/reservations/<int:booking_id>")
@admin_required
def booking_detail(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template("admin/bookings/detail.html", booking=booking)


@bp.route("/reservations/<int:booking_id>/statut", methods=["POST"])
@admin_required
def booking_update_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get("status")
    if new_status in ("pending", "confirmed", "cancelled", "completed"):
        booking.status = new_status
        db.session.commit()
        flash(f"Statut mis à jour : {new_status}", "success")
    return redirect(url_for("admin.booking_detail", booking_id=booking_id))
