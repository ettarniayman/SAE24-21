from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import current_user
from . import bp, admin_required
from ...extensions import db
from ...models.media import Media
from ...models.destination import Destination
from ...models.hotel import Hotel
from ...utils.helpers import save_uploaded_file
import os

_IMAGE_EXTS = {"jpg", "jpeg", "png", "webp", "gif"}
_VIDEO_EXTS = {"mp4", "webm", "mov"}


@bp.route("/medias")
@admin_required
def media_list():
    page = request.args.get("page", 1, type=int)
    medias = Media.query.order_by(Media.created_at.desc()).paginate(page=page, per_page=24)
    destinations = Destination.query.order_by(Destination.name_fr).all()
    hotels = Hotel.query.order_by(Hotel.name).all()
    return render_template("admin/media/list.html", medias=medias.items, pagination=medias,
                           destinations=destinations, hotels=hotels)


@bp.route("/medias/upload", methods=["POST"])
@admin_required
def media_upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file"}), 400
    filename = save_uploaded_file(file, "uploads")
    if not filename:
        return jsonify({"error": "Extension non autorisée (jpg/png/webp/gif/mp4/webm/mov/pdf)"}), 400

    ext = filename.rsplit(".", 1)[-1].lower()
    if ext in _IMAGE_EXTS:
        file_type = "image"
    elif ext in _VIDEO_EXTS:
        file_type = "video"
    else:
        file_type = "document"

    dest_id = request.form.get("destination_id", type=int)
    hotel_id = request.form.get("hotel_id", type=int)
    category = request.form.get("media_category", "gallery")

    full_path = os.path.join(current_app.root_path, "static", "images", "uploads", filename)
    file_size = os.path.getsize(full_path) if os.path.exists(full_path) else None

    media = Media(
        filename=filename,
        original_name=file.filename,
        file_path=f"/static/images/uploads/{filename}",
        file_type=file_type,
        mime_type=file.content_type or None,
        file_size=file_size,
        file_size_kb=round(file_size / 1024) if file_size else None,
        media_category=category,
        destination_id=dest_id,
        hotel_id=hotel_id,
        uploaded_by=current_user.id,
    )
    db.session.add(media)
    db.session.commit()
    return jsonify({"success": True, "path": media.file_path, "id": media.id, "type": file_type})


@bp.route("/medias/add-url", methods=["POST"])
@admin_required
def media_add_url():
    video_url = request.form.get("video_url", "").strip()
    if not video_url or not video_url.startswith("http"):
        flash("URL externe invalide.", "danger")
        return redirect(url_for("admin.media_list"))

    dest_id = request.form.get("destination_id", type=int)
    hotel_id = request.form.get("hotel_id", type=int)
    category = request.form.get("media_category", "gallery")
    title_fr = request.form.get("title_fr", "").strip() or None

    media = Media(
        video_url=video_url,
        file_type="video",
        title_fr=title_fr,
        media_category=category,
        destination_id=dest_id,
        hotel_id=hotel_id,
        uploaded_by=current_user.id,
    )
    db.session.add(media)
    db.session.commit()
    flash("Vidéo externe ajoutée.", "success")
    return redirect(url_for("admin.media_list"))


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
