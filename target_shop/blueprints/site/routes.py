from flask import Blueprint, flash, redirect, render_template, request

# Internal imoprts
from target_shop.models import Product, db
from target_shop.forms import ProductForm

# Instantiating my blueprint class
site = Blueprint('site', __name__, template_folder='site_templates' )


#using the site object to create routes
@site.route('/')
def shop():

    allprods = Product.query.all()




    return render_template('shop.html', shop=allprods)

@site.route('/shop/create', methods=['GET', 'POST'])
def create():

    createform = ProductForm()

    if request.method == 'POST' and createform.validate_on_submit():
        name = createform.name.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data

        product = Product(name, price, quantity, image, description)

        db.session.add(product)
        db.session.commit()

        flash(f"You have succesfully added products {name}", category='success')
        return redirect('/')

    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/shop/create')
    
    return render_template('create.html', form=createform)

@site.route('/shop/update/<id>', methods=['GET', 'POST'])
def update(id):

    product= Product.query.get(id)

    updateform = ProductForm()

    if request.method == 'POST' and update.form.validate_on_submit():
        product.name = updateform.name.data 
        product.image = product.image = product.set_image(updateform.image.data, updateform.name.data)
        product.description = updateform.description.data 
        product.price = updateform.price.data 
        product.quantity = updateform.quantity.data

        db.session.commit()

        flash(f"You have successfully updated products {product.name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect(f'/shop/update/{product.product_id}')
    
    return render_template('update.html', form=updateform, product=product )

@site.route('/shop/delete/<id>')
def delete(id):
    
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')
