import os
from flask import Flask, render_template, request, g
from .extensions import db, login_manager, csrf, migrate, mail, babel
from config import config_map


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map["default"]))

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "warning"

    # Import models so Flask-Migrate sees them
    from .models import (
        user, country, destination, activity, hotel, program,
        airline, testimonial, blog, contact, newsletter, faq,
        promotion, media, shop, booking, rss_item
    )

    # Blueprints
    from .routes.main import bp as main_bp
    from .routes.destinations import bp as dest_bp
    from .routes.programs import bp as prog_bp
    from .routes.hotels import bp as hotels_bp
    from .routes.airlines import bp as airlines_bp
    from .routes.blog import bp as blog_bp
    from .routes.shop import bp as shop_bp
    from .routes.contact import bp as contact_bp
    from .routes.auth import bp as auth_bp
    from .routes.rss import bp as rss_bp
    from .routes.api import bp as api_bp
    from .routes.admin import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(dest_bp, url_prefix="/destinations")
    app.register_blueprint(prog_bp, url_prefix="/programmes")
    app.register_blueprint(hotels_bp, url_prefix="/hotels")
    app.register_blueprint(airlines_bp, url_prefix="/compagnies")
    app.register_blueprint(blog_bp, url_prefix="/blog")
    app.register_blueprint(shop_bp, url_prefix="/boutique")
    app.register_blueprint(contact_bp, url_prefix="/contact")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(rss_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Create tables if they don't exist (dev / first boot)
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            db.session.rollback()

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    # Context processors
    @app.context_processor
    def inject_globals():
        from .models.destination import Destination
        from .models.promotion import Promotion
        from .models.rss_item import RSSItem
        featured = Destination.query.filter_by(is_featured=True).limit(6).all()
        active_promos = Promotion.query.filter_by(is_active=True).limit(3).all()
        latest_news = RSSItem.query.order_by(RSSItem.published_at.desc()).limit(5).all()
        return dict(
            featured_destinations=featured,
            active_promotions=active_promos,
            latest_news=latest_news,
            google_maps_api_key=app.config.get("GOOGLE_MAPS_API_KEY", ""),
            current_lang=get_locale(),
        )

    return app


def get_locale():
    lang = request.args.get("lang") or request.cookies.get("lang")
    if lang in ["fr", "en"]:
        return lang
    return "fr"
