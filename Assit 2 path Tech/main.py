from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL

 
 
app = Flask(__name__)
app.secret_key = 'ideafoundation'
 
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'assist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


try:
    conn = mysql.connect()
    cursor =conn.cursor()
except Exception as e:
    print("Error:",e)


@app.route('/',methods=["GET"])
def home():
    fetch_all="select * from product"
    cursor.execute(fetch_all)
    product=cursor.fetchall()
    return render_template('index.html',product=product)

@app.route("/edit",methods=["GET","POST"])
def edit_product():
    id_value=request.form["id_value"]
    name=request.form["name"]
    price=int(request.form["price"])
    quantity=int(request.form["quantity"])
    update_product=f"update product set name='{name}', price={price}, quantity={quantity} where id={id_value}"
    cursor.execute(update_product)
    cursor.execute("commit")
    fetch_updated="select * from product"
    cursor.execute(fetch_updated)
    product=cursor.fetchall()
    return render_template('index.html',product=product)
    

@app.route("/create",methods=["GET","POST"])
def create_product():
    name=request.form["name"]
    price=int(request.form["price"])
    quantity=int(request.form["quantity"])
    add_product=f"insert into product (name,price,quantity) values ('{name}',{price},{quantity})"
    cursor.execute(add_product)
    cursor.execute("commit")
    fetch_updated="select * from product"
    cursor.execute(fetch_updated)
    product=cursor.fetchall()
    return render_template('index.html',product=product)

@app.route("/search",methods=["GET","POST"])
def search_product():
    search_str=request.form['search_data']
    if search_str=="":
        search_product="select * from product"
    else:
        search_str=search_str+'%'
        search_product=f"select * from product where name like '{search_str}'"
        
    cursor.execute(search_product)
    product=cursor.fetchall()
    return render_template('index.html',product=product)
    
    
if __name__=='__main__':
    app.run(debug=False)
