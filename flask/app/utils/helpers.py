import os
import secrets
import bleach
from datetime import datetime, timezone
from flask import current_app, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "pdf"}
ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "a", "h2", "h3", "h4", "blockquote"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file, subfolder="uploads"):
    if not file or not allowed_file(file.filename):
        return None
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secrets.token_hex(16) + "." + ext
    upload_dir = os.path.join(current_app.root_path, "static", "images", subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return filename


def sanitize_html(content):
    return bleach.clean(content, tags=ALLOWED_TAGS, strip=True)


def generate_sitemap():
    from ..models.destination import Destination
    from ..models.program import TravelProgram
    from ..models.blog import BlogPost
    from ..models.hotel import Hotel

    base_url = "https://rtvoyage.com"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    urls = [
        f"<url><loc>{base_url}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>",
        f"<url><loc>{base_url}/destinations/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>",
        f"<url><loc>{base_url}/programmes/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>",
        f"<url><loc>{base_url}/hotels/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>",
        f"<url><loc>{base_url}/blog/</loc><changefreq>daily</changefreq><priority>0.8</priority></url>",
        f"<url><loc>{base_url}/boutique/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>",
        f"<url><loc>{base_url}/contact/</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>",
        f"<url><loc>{base_url}/faq</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>",
    ]

    for dest in Destination.query.filter_by(is_active=True).all():
        urls.append(
            f"<url><loc>{base_url}/destinations/{dest.slug}</loc>"
            f"<lastmod>{dest.updated_at.strftime('%Y-%m-%d') if dest.updated_at else now}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>0.8</priority></url>"
        )

    for prog in TravelProgram.query.filter_by(is_active=True).all():
        urls.append(f"<url><loc>{base_url}/programmes/{prog.slug}</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>")

    for post in BlogPost.query.filter_by(is_published=True).all():
        urls.append(f"<url><loc>{base_url}/blog/{post.slug}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""
    return xml
