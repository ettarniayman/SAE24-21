from flask import render_template, request
from . import bp, admin_required
from ...models.newsletter import NewsletterSubscriber


@bp.route("/newsletter")
@admin_required
def newsletter_list():
    page = request.args.get("page", 1, type=int)
    subs = NewsletterSubscriber.query.filter_by(is_active=True).order_by(
        NewsletterSubscriber.subscribed_at.desc()
    ).paginate(page=page, per_page=30)
    total = NewsletterSubscriber.query.filter_by(is_active=True).count()
    return render_template("admin/newsletter/list.html", subs=subs.items, pagination=subs, total=total)
