from flask import render_template, redirect, url_for, flash, request
from . import bp, admin_required
from ...extensions import db
from ...models.booking import Booking


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
