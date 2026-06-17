from flask import render_template, request, jsonify
from . import bp, admin_required
from ...extensions import db
from ...models.order import Order

VALID_STATUSES = ("pending", "confirmed", "paid", "processing", "completed", "cancelled", "refunded")
VALID_PAYMENT_STATUSES = ("pending", "paid", "refunded", "failed")


@bp.route("/commandes")
@admin_required
def order_list():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status", "")
    query = Order.query
    if status:
        query = query.filter_by(status=status)
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/orders/list.html", orders=orders.items, pagination=orders, current_status=status)


@bp.route("/commandes/<int:order_id>")
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("admin/orders/detail.html", order=order)


@bp.route("/commandes/<int:order_id>/statut", methods=["POST"])
@admin_required
def order_update_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json(silent=True) or request.form
    new_status = data.get("status")
    new_payment_status = data.get("payment_status")

    if new_status and new_status in VALID_STATUSES:
        order.status = new_status
    if new_payment_status and new_payment_status in VALID_PAYMENT_STATUSES:
        order.payment_status = new_payment_status

    db.session.commit()
    return jsonify({
        "success": True,
        "status": order.status,
        "payment_status": order.payment_status,
    })
