from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user
from ..extensions import db
from ..models.program import TravelProgram
from ..models.shop import ShopProduct
from ..models.order import Order, OrderItem

bp = Blueprint("cart", __name__)

SESSION_KEY = "cart"


def _get_cart():
    return session.setdefault(SESSION_KEY, [])


def _save_cart(cart):
    session[SESSION_KEY] = cart
    session.modified = True


def _cart_count():
    return sum(item.get("quantity", 1) for item in session.get(SESSION_KEY, []))


def _enrich_cart_items(cart):
    """Recharge les objets Program/Product et calcule les sous-totaux pour l'affichage."""
    enriched = []
    subtotal = 0
    for item in cart:
        if item["item_type"] == "program":
            obj = TravelProgram.query.get(item["program_id"])
            if not obj:
                continue
            unit_price = float(obj.price_per_person_discounted or obj.price_per_person or 0)
            name = obj.name_fr
        else:
            obj = ShopProduct.query.get(item["product_id"])
            if not obj:
                continue
            unit_price = float(obj.price_discounted or obj.price)
            name = obj.name_fr
        line_subtotal = unit_price * item.get("quantity", 1)
        subtotal += line_subtotal
        enriched.append({
            **item,
            "object": obj,
            "name": name,
            "unit_price": unit_price,
            "subtotal": line_subtotal,
        })
    return enriched, subtotal


@bp.route("/")
def view():
    cart = _get_cart()
    items, subtotal = _enrich_cart_items(cart)
    return render_template("cart/view.html", items=items, subtotal=subtotal)


@bp.route("/ajouter", methods=["POST"])
def add():
    item_type = request.form.get("item_type")
    cart = _get_cart()

    if item_type == "program":
        program_id = request.form.get("program_id", type=int)
        program = TravelProgram.query.get_or_404(program_id)
        departure_date = request.form.get("departure_date") or None
        participants = request.form.get("participants", 1, type=int)
        cart.append({
            "item_type": "program",
            "program_id": program.id,
            "quantity": 1,
            "departure_date": departure_date,
            "participants": participants,
        })
        flash(f"« {program.name_fr} » ajouté au panier.", "success")
    elif item_type == "product":
        product_id = request.form.get("product_id", type=int)
        product = ShopProduct.query.get_or_404(product_id)
        quantity = request.form.get("quantity", 1, type=int)
        cart.append({
            "item_type": "product",
            "product_id": product.id,
            "quantity": max(1, quantity),
        })
        flash(f"« {product.name_fr} » ajouté au panier.", "success")
    else:
        flash("Article invalide.", "danger")
        return redirect(request.referrer or url_for("main.index"))

    _save_cart(cart)
    return redirect(request.referrer or url_for("cart.view"))


@bp.route("/retirer", methods=["POST"])
def remove():
    index = request.form.get("index", type=int)
    cart = _get_cart()
    if index is not None and 0 <= index < len(cart):
        cart.pop(index)
        _save_cart(cart)
        flash("Article retiré du panier.", "success")
    return redirect(url_for("cart.view"))


@bp.route("/vider", methods=["POST"])
def clear():
    _save_cart([])
    flash("Panier vidé.", "success")
    return redirect(url_for("cart.view"))


@bp.route("/commander", methods=["POST"])
def checkout():
    cart = _get_cart()
    items, subtotal = _enrich_cart_items(cart)
    if not items:
        flash("Votre panier est vide.", "danger")
        return redirect(url_for("cart.view"))

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    billing_address = request.form.get("billing_address", "").strip()

    if not (first_name and last_name and email):
        flash("Merci de renseigner vos coordonnées (nom, prénom, email).", "danger")
        return redirect(url_for("cart.view"))

    order = Order(
        user_id=current_user.id if current_user.is_authenticated else None,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        billing_address=billing_address,
        status="pending",
        payment_status="pending",
        subtotal=subtotal,
        total=subtotal,
    )
    db.session.add(order)
    db.session.flush()

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            item_type=item["item_type"],
            program_id=item.get("program_id"),
            product_id=item.get("product_id"),
            quantity=item.get("quantity", 1),
            unit_price=item["unit_price"],
            departure_date=item.get("departure_date") or None,
            participants=item.get("participants"),
            subtotal=item["subtotal"],
        )
        db.session.add(order_item)

    db.session.commit()
    _save_cart([])

    flash(
        f"Commande {order.reference} enregistrée. Un conseiller vous contactera pour le paiement.",
        "success",
    )
    return redirect(url_for("cart.confirmation", reference=order.reference))


@bp.route("/confirmation/<reference>")
def confirmation(reference):
    order = Order.query.filter_by(reference=reference).first_or_404()
    return render_template("cart/confirmation.html", order=order)
