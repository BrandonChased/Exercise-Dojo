from flask_app import app
from flask import render_template,redirect,session,flash,request
from flask_app.models.product_model import Product


#****************** DASHBOARD PAGE ******************
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/")
    
    products = Product.get_all_products()

    return render_template("dashboard.html" , products = products)

#****************** Category PAGE ******************
@app.route("/category/<int:id>")
def category(id):
    if "email" not in session:
        return redirect("/")
    
    products = Product.get_all_products_in_category(id)

    return render_template("category.html" , products = products)

#***************** ADD ITEM TO CART ******************

@app.route("/add/item/to_cart", methods=["POST"])
def add_item_to_cart():
    if "email" not in session:
        return redirect("/")


    item = Product.get_product(request.form)

    cart_list = session["cart"]
    cart_list.append(item)

    session["cart"] = cart_list

    return redirect("/checkout")


#****************** VIEW ITEM PAGE  ******************


@app.route("/view/<int:id>")
def view_item(id):
    if "email" not in session:
        return redirect("/")


    data = {
        "id" : id
    }

    product = Product.get_product_cls(data)

    return render_template("product.html", product = product)

#****************** CHECKOUT PAGE  ******************

@app.route("/checkout")
def checkout():
    if "email" not in session:
        return redirect("/")
    
    cart = session["cart"]

    return render_template("cart.html",cart = cart)


#****************** CLEAR CART  ******************

@app.route("/clear/cart")
def clear_cart():
    session["cart"] = []

    return redirect("/checkout")