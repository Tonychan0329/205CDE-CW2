from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
app = Flask(__name__)
app.secret_key= 'random string'

# open database connection
db = pymysql.connect("localhost", "tony", "Tony15987456", "eshop") 

#Home page
@app.route('/home')
@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM product')
    data = cursor.fetchall()
    return render_template('index.html', output_data = data)

#about page
@app.route('/about')
def about():
    return render_template('about.html')

#gallery page
@app.route('/gallery')
def gallery():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM product ")
    data = cursor.fetchall()
    return render_template('gallery.html', output_data = data)
    
#search function
@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search = request.form["search"]

        cursor = db.cursor()
        cursor.execute("""SELECT * FROM product WHERE name like %s """, (search))
        data = cursor.fetchall()

        return render_template('search.html', output_data = data)
    return render_template('search.html')


#account/profile page
@app.route('/account/profile')
def profile():
    if 'email' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = '" + session['email'] + "'")
        data = cursor.fetchall()
        return render_template('user_profile.html', userdata = data )
    return redirect(url_for('login'))

@app.route('/account/profile/edit')
def editprofile():
    msg = ''
    if 'email' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = '" + session['email'] + "'")
        profileData = cursor.fetchone()
        return render_template("edit_profile.html", profileData=profileData)
    return redirect(url_for('login'))

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    msg=''
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        newPassword = request.form['newpassword']
        
        cursor = db.cursor()
        cursor.execute("SELECT user_id, password FROM users WHERE email = '" + session['email'] + "'")
        user_id, password = cursor.fetchone()
        if (password == oldPassword):
            try:
                cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (newPassword, user_id))
                db.commit()
                msg="Changed successfully"
            except:
                db.rollback()
                msg = "Failed"
            return render_template("changepassword.html", msg=msg)
        else:
            msg = "Wrong password"
        
    return render_template("changepassword.html", msg=msg) 
    db.close()

#show product
@app.route('/products')
def showproduct():
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product ")
        data = cursor.fetchall()
        return render_template('products.html', output_data = data)
    else:
        return redirect(url_for('login'))

#productdetail
@app.route("/productdetail")
def productdetail():
    productId = request.args.get('productId')
    
    cursor = db.cursor()
    cursor.execute('SELECT * FROM product WHERE pd_id = ' + productId)
    productData = cursor.fetchone()
    return render_template("productdetail.html", data=productData)
    db.close()

#update profile action
@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        city = request.form['city']
        country = request.form['country']
        address = request.form['address']
        phone = request.form['phone_number']
                
        cur = db.cursor()
        cur.execute("""UPDATE users SET firstName = %s, lastName = %s, address = %s, city = %s, country = %s, phone = %s WHERE email = %s""", (firstName, lastName, address, city, country, phone, email))

        try:
            db.commit()
            msg = "Saved Successfully"
        except:
            db.rollback()
            msg = "Error occured"
        
    return redirect(url_for('editprofile', msg = msg))
    db.close()

#reservation form action
@app.route('/reservation')
def reservation():
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM product ")
        data = cursor.fetchall()
        return render_template('reservation.html', output_data = data)
    return redirect(url_for('login'))

@app.route('/reservation/submit', methods=['POST', 'GET'])
def reservation_submit():
        msg = ''
        if request.method == 'POST':

            email = request.form['email']
            phone = request.form['phone']
            product = request.form['product']
            amount = request.form['amount']

            cursor = db.cursor()
            cursor.execute("""INSERT INTO reservation(reser_user_email, reser_phone, pd_name, reser_amount) VALUES (%s, %s, %s, %s)""", (email, phone, product, amount))

            try:
                db.commit()
                msg = "Your reservation is uploaded, you will receive the phone message as soon as possible !"
            except Exception as e:
                db.rollback()
                msg = "Error Occured"
        return render_template('reservation.html', msg = msg)
        db.close()

#register form action
@app.route("/cust_reg", methods = ["POST", "GET"])
def register():
    msg = ''
    if request.method == 'POST':
        
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone_number']

        cursor = db.cursor()
        cursor.execute("""insert into users(password, email, firstName, lastName, address, city, country, phone) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (password, email, firstName, lastName, address, city, country, phone))

        try:
            db.commit()
            msg = "Information is successfully inserted !"
        except Exception as e:
            db.rollback()
            msg = "Error occured"
    return render_template("cust_reg.html", msg=msg)
    db.close()

#login form action
@app.route("/cust_login", methods = ["POST", "GET"])
def login():
    error = ''
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor() 
        cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s ',(email, password))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['email'] = email
            return redirect(url_for("showproduct"))
        else:
            error = 'Invalid User Email / Password'

    return render_template("cust_login.html", error = error)

#shopping cart page#
@app.route('/cart')
def cart():
    if 'email' in session:
        cursor = db.cursor()
        cursor.execute("SELECT cart.cart_id, product.name, product.image, product.price FROM cart LEFT JOIN product ON cart.productId = product.pd_id ORDER BY cart.cart_id  ")
        data = cursor.fetchall()
        totalPrice = 0
        for row in data:
            totalPrice += row[3]
        return render_template('shoppingcart.html', output_data = data, totalPrice=totalPrice)
    else:
        return redirect(url_for('login'))

#add item to cart action
@app.route('/addToCart')
def addtocart():
    msg = ''
    if 'email' in session:
        productId = int(request.args.get('productId'))
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = '" + session['email'] + "'")
        userId = cursor.fetchone()
        try:
            cursor.execute("INSERT INTO cart (userId, productId) VALUES (%s, %s)", (userId, productId))
            db.commit()
            msg = "Added successfully"
        except:
            db.rollback()
            msg = "Error occured"
    cursor.close()        
    return redirect(url_for('cart', msg= msg))

#remove item from cart action
@app.route('/removeFromCart', methods=['POST'])
def removefromcart():
    if 'email' in session:
        productId = int(request.args.get('productId'))
        email = session['email']
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = '" + email + "'")
        userId = cursor.fetchone()
        try:
            cursor.execute("""DELETE FROM `cart` WHERE `cart`.`cart_id` = %s""", productId )
            db.commit()
            msg = "removed successfully"
        except:
            db.rollback()
            msg = "error occured"
    cursor.close()
    return redirect(url_for('cart', msg= msg))

#admin login form action
@app.route("/admin_login", methods = ["POST", "GET"])
def adminlogin():
    error = ''
    if request.method == "POST":
        admin_email = request.form['admin_email']
        admin_password = request.form['admin_password']

        cursor = db.cursor() 
        cursor.execute('SELECT * FROM admin WHERE admin_email=%s AND admin_password=%s',(admin_email, admin_password))
        admin = cursor.fetchone()
        if admin:
            session['adminLoggedin'] = True
            session['adminemail'] = admin_email
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Adminemail / Password'

    return render_template("Admin_login.html", error = error)

#admin dasborad page
@app.route('/dashboard')
def dashboard():
    if 'adminLoggedin' in session:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM product')
        data = cursor.fetchall()
        return render_template('Admin_index.html', output_data = data)
    else:
        return redirect(url_for('adminlogin'))

#userinfo page & show users detail
@app.route('/userinfo')
def userinfo():
    if 'adminLoggedin' in session:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users')
        data = cursor.fetchall()
        return render_template('user_info.html', output_data = data)
    else:
        return redirect(url_for('adminlogin'))

#order page & show order detail
@app.route('/userReservation')
def userReservation():
    if 'adminLoggedin' in session:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM reservation')
        data = cursor.fetchall()
        return render_template('userReservation.html', output_data = data)
    else:
        return redirect(url_for('adminlogin'))

#admin add item page
@app.route('/addproduct')
def add():
    if 'adminLoggedin' in session:
        return render_template('admin_add.html')
    else:
        return redirect(url_for('adminlogin'))

#admin add item form action 
@app.route('/addItem', methods=["POST", "GET"])
def addItem():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        price = request.form['price']
        description = request.form['description']
        stock = request.form['stock']
        image = request.form['image']
        status = request.form['status']

        cursor = db.cursor()
        cursor.execute("""insert into product(name, code, price, description, stock, image, status ) values (%s, %s, %s, %s, %s, %s, %s)""", (name, code, price, description, stock, image, status))

        try:
            db.commit()
            msg = "Product Update Complete !"
        except Exception as e:
            db.rollback()
            mag = "Error Occured"
    return render_template("admin_add.html", msg = msg)
    db.cloce()    

@app.route('/product/edit')
def editproduct():
    if 'adminLoggedin' in session:
        productId = request.args.get('productId')
    
        cursor = db.cursor()
        cursor.execute('SELECT * FROM product WHERE pd_id = ' + productId)
        productData = cursor.fetchone()
        return render_template("editproduct.html", data=productData)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/product/update', methods=["POST", "GET"])
def updateproduct():
    msg = ''
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        code = request.form['code']
        image = request.form['image']
        price = request.form['price']
        stock = request.form['stock']
        description = request.form['description']
        status = request.form['status']

        cursor = db.cursor()
        cursor.execute("UPDATE product SET name= %s, code=%s, image=%s, price=%s, stock=%s, description=%s, status=%s WHERE pd_id = %s",(name, code, image, price, stock, description, status, id))
        try:
            db.commit()
            msg = "Saved Successfully"
        except:
            db.rollback()
            msg = "Error occured"
        
    return redirect(url_for('dashboard', msg = msg))
    db.close()

@app.route('/delete_product', methods=['POST'])
def delete_product():
    productId = request.args.get('productId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE pd_id = " + productId )
    db.commit()
    cursor.close()
    return redirect(url_for('dashboard'))

@app.route('/delete_reservation', methods=['POST'])
def delete_reservation():
    reservationId = request.args.get('reservationId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM reservation WHERE reser_id = " + reservationId )
    db.commit()
    cursor.close()
    return redirect(url_for('userReservation'))

@app.route('/admin/order')
def adminorder():
    if 'adminLoggedin' in session:

        cursor = db.cursor()
        cursor.execute('SELECT cart.cart_id, users.email, users.firstName, users.lastName, product.image FROM ((cart LEFT JOIN users ON cart.userId = users.user_id) LEFT JOIN product ON cart.productID = product.pd_id) ORDER BY users.email')
        data = cursor.fetchall()
        return render_template('admin_order.html', output_data = data)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/checkout/process')
def check_process():
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT cart.cart_id, product.name, product.image, product.price FROM cart LEFT JOIN product ON cart.productId = product.pd_id ORDER BY cart.cart_id  ")
        data = cursor.fetchall()
        totalPrice = 0
        for row in data:
            totalPrice += row[3]
        return render_template('checkout.html', output_data = data, totalPrice=totalPrice)
    else:
        return redirect(url_for('login'))

@app.route('/checkout/complete')
def check_complete():
    if 'loggedin' in session:
        cursor = db.cursor()
        cursor.execute("SELECT firstName, lastName FROM users WHERE email = '" + session['email'] + "'")
        data = cursor.fetchall()
        return render_template('complete.html', output_data = data)
    return redirect(url_for('login'))

@app.route('/delete_order', methods=['POST'])
def delete_order():
    cartId = request.args.get('cartId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM cart WHERE cart_id = " + cartId )
    db.commit()
    cursor.close()
    return redirect(url_for('adminorder'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    userId = request.args.get('userId')
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = " + userId )
    db.commit()
    cursor.close()
    return redirect(url_for('userinfo'))

#user & admin Logout action 
@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return render_template('cust_login.html')

@app.route("/adminlogout")
def adminlogout():
    session.pop('adminLoggedin', None)
    session.pop('adminemail', None)
    return render_template('Admin_login.html')

if __name__ == '__main__':
    app.run(debug = True)
    

