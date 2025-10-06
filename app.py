from flask import Flask, render_template, request, redirect, flash, session
import sqlite3
from sqlite3 import Error;
import logging

def get_db_connection():
# Creating connection to databasepip3
  conn = None;

  try:
      # Attempt to connect to the database
      conn = sqlite3.connect("assets/shopped_data.db");
      print("---------------------------------------------------------------")
      print("[LOG] - Connected to database. Version", sqlite3.version);
  # If there is no connection, print an error
  except Error as er:
      print(er);

  # Enable row factory
  conn.row_factory = sqlite3.Row;

   # Enforce referential Integrity
  sql = """
          PRAGMA foreign_keys = ON
          """
  conn.execute(sql);
  return conn

# Code from last year, irrelevant for this internal
def get_items(searchinput, sortvar, sortcolumn):
  # Establish connection to the database and grab the cursor
  conn = get_db_connection()
  cur = conn.cursor()
  # Rewrite the string list to remove the apostrophes so that it can work in the SQL function
  print("[LOG] - Attempting to execute SQL function")
    # Each function is put into place in the SQL code
  sql = f"""
  SELECT * FROM tbl_items
  WHERE (id LIKE '%{searchinput}%'
  OR name LIKE '%{searchinput}%'
  OR cost LIKE '%{searchinput}%'
  OR image LIKE '%{searchinput}%'
  OR stock LIKE '%{searchinput}%')
  ORDER BY {sortcolumn} {sortvar}
  """
  # Execute the SQL code and update the table
  changed_table = cur.execute(sql).fetchall()
  print(f"[LOG] - Table has been updated. Sort type: {sortvar}, column sorted: {sortcolumn}, search input: {searchinput}.")
  print("---------------------------------------------------------------")
  conn.close()

  return changed_table;

def cat_description_get():
    # Establish connection to the database and grab the cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetching all content from tbl_items, filters, and filters_names
    all_items = cur.execute('SELECT * FROM tbl_items').fetchall()
    all_categories = cur.execute('SELECT * FROM tbl_filters').fetchall()
    all_filters = cur.execute('SELECT * FROM tbl_filters_names').fetchall()
    all_carts = cur.execute('SELECT * FROM tbl_carts').fetchall()
    all_purchs = cur.execute('SELECT * FROM tbl_purchs').fetchall()
    all_purchs_items = cur.execute('SELECT * FROM tbl_purchs_items').fetchall()
    print("[LOG] - All relevant tables have been selected")
    print("---------------------------------------------------------------")
    cur.close()
    
    return all_items, all_categories, all_filters, all_carts, all_purchs, all_purchs_items

# Adding to cart function
def add_cart(c_data):
    conn = get_db_connection()
    sql = """INSERT INTO tbl_carts
    (userid, product)
    VALUES(?,?)
    """
    conn.execute(sql, c_data)
    print(f"[LOG] - Added item to cart with id and product id: {c_data}")
    conn.commit()
    conn.close()

# Function to update an item
def update_item(i_name):
    # Establishing a connection to the database
	conn = get_db_connection()
    # Code to execute in SQL
	sql = """
            UPDATE tbl_items SET
            name = ?,
            cost = ?,
            image = ?,
            stock = ?
            WHERE id = ?
            """
    # Execute the SQL code using the values in i_name
	conn.execute(sql, i_name).rowcount
	print(f"[LOG] - Updated item with name and values: {i_name}")
    # Committing the current action
	conn.commit()
    # Closing connection to database
	conn.close()

def update_name(n_name):
	conn = get_db_connection()
	sql = """
            UPDATE tbl_filters_names SET
            name = ?
            WHERE id = ?
            """
	conn.execute(sql, n_name)
	print(f"[LOG] - Updated filter name with title and ID: {n_name}")
	conn.commit()
	conn.close()

# Function to add an item
def add_item(i_data):
    conn = get_db_connection()
    # The sql execute code is change from update fields to adding fields
    sql = """
    INSERT INTO tbl_items 
    (name, cost, image, stock) 
    VALUES(?,?,?,?)"""
    # Execute the sql code with i_data while also using the lastrowid in order to make the new primary key ID
    conn.execute(sql, i_data).lastrowid    
    print(f"[LOG] - Added new item with name and values: {i_data}")
    conn.commit()
    conn.close()

def add_filter(f_data):
    conn = get_db_connection()
    sql = """
    INSERT INTO tbl_filters 
    (id, name_id) 
    VALUES(?,?)"""
    conn.execute(sql, f_data)
    print(f"[LOG] - Added new filter with values: {f_data}")
    conn.commit()
    conn.close()

def add_name(n_data):
    conn = get_db_connection()
    sql = """
    INSERT INTO tbl_filters_names (name) VALUES(?)
    """
    conn.execute(sql, (n_data,)).lastrowid
    print(f"[LOG] - Added new filter name with title and ID: {n_data}")
    conn.commit()
    conn.close()

def remove_name(n_item):
    conn = get_db_connection()
    sql = """
    DELETE FROM tbl_filters_names WHERE id = ? AND name = ?;
    """
    conn.execute(sql, (n_item,))
    print(f"[LOG] - Removed filter name with ID and name: {n_item}")
    conn.commit()
    conn.close()

def remove_filter(f_item):
    sql = """
    DELETE FROM tbl_filters WHERE id = ? AND name_id = ?;
    """
    conn = get_db_connection()
    cur = conn.cursor();
    remove_filter_id = cur.execute(sql, (f_item,))
    print(f"[LOG] - Removed filter named: {remove_filter_id}")
    conn.commit()
    conn.close()

def remove_purchase(p_item):
    print("[LOG] - Attempting to remove a purchase")
    sql = """
    DELETE FROM tbl_purchs WHERE id = ?;
    """
    conn = get_db_connection()
    cur = conn.cursor();
    remove_purchs_id = cur.execute(sql, (p_item,))
    print(f"[LOG] - Removed purchase with id: {remove_purchs_id}")
    conn.commit()
    conn.close()

def remove_purchase_item(p_item):
    print("[LOG] - Attempting to remove a purchase item")
    sql = """
    DELETE FROM tbl_purchs_items WHERE purchase_id = ? AND item_id = ?;
    """
    conn = get_db_connection()
    cur = conn.cursor();
    remove_pitem_id = cur.execute(sql, p_item)
    print(f"[LOG] - Removed item with id: {remove_pitem_id}")
    conn.commit()
    conn.close()

# Function to delete an item
def remove_item(i_item):
    # Deleting from the database using the DELETE function now
    sql = """
    DELETE FROM tbl_items WHERE id = ?;
    """
    conn = get_db_connection()
    cur = conn.cursor();
    remove_name_id = cur.execute(sql, (i_item,))
    print(f"[LOG] - Removed item with id: {remove_name_id}")
    conn.commit()
    conn.close()

def remove_cart(c_item):
    print("LOG - Attempting to delete an item from cart")
    sql = """
    DELETE FROM tbl_carts WHERE userid = ? AND product = ?;
    """
    conn = get_db_connection()
    cur = conn.cursor();
    remove_cart_id = cur.execute(sql, c_item)
    print(f"[LOG] - Removed item with id: {remove_cart_id}")
    conn.commit()
    conn.close()
    
def add_order(user_id, cart_items, total):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Find new purchase id
    cursor.execute("SELECT MAX(id) FROM tbl_purchs")
    last_id = cursor.fetchone()[0]
    if last_id is None:
        new_id = 1
    else:
        new_id = last_id + 1

    cursor.execute(
        "INSERT INTO tbl_purchs (id, total, user) VALUES (?, ?, ?)",
        (new_id, total, user_id)
    )

    # Insert into tbl_purchs_items
    for c in cart_items:
        product_id = c['product']
        cursor.execute(
            "INSERT INTO tbl_purchs_items (purchase_id, item_id) VALUES (?, ?)",
            (new_id, product_id)
        )

    # Clear user's cart
    cursor.execute(
        "DELETE FROM tbl_carts WHERE userid = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()



app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Encrypts the data in the session, this is irrelevant so there is a placeholder for now
app.config['SECRET_KEY'] = 'secret_key_placeholder'

# When there is no set @app.route, automatically route to /login
@app.route("/",methods=['GET', 'POST'])
def default():
   print("[LOG] - No route, redirecting to login")
   return redirect("/login")

# App route for the login page, contains the login function.
@app.route('/home', methods=['GET', 'POST'])
def home():
    role = session.get('role', None)
    print("[LOG] - Arrived at home page")
    if request.form.get('action') == 'login':
       return redirect('/login')
    if request.form.get('action') == 'admin':
       return redirect('/admin')
    if request.form.get('action') == 'account':
       return redirect('/account')
    return render_template("home.html", role=role)


# Shop app route
@app.route('/shop', methods=['GET', 'POST'])
def index():
    
    role = session.get('role', None)  # None if not logged in
    user = session.get('id', None)
    if request.form.get('action') == 'login':
       return redirect('/login')
    if request.form.get('action') == 'admin':
       return redirect('/admin')
    if request.form.get('action') == 'account':
       return redirect('/account')


    # Default values for when the page initially loads
    sortcolumn = 'id'
    sortvar = 'ASC'
    searchinput = ''
    # Execute this function when the page first loads without an action so that there is a table
    data = get_items(searchinput, sortvar, sortcolumn)

    if request.method == 'POST':
        print("[LOG] - POST request detected")
        # Find which type of action has been chosed
        action = request.form.get("action")
        print(f"[LOG] - Action type received: {action}")
        # Find values for all variables. Ones that do not have any values are assigned the next one over.
        # E.g if there is no value for sortMethod, sortMethod = ASC.
        searchinput = request.form.get("search", "")
        sortvar = request.form.get("sortMethod", "ASC")
        sortcolumn = request.form.get("sortColumn", "id")

        # For all other action types, execute function get_items().
        if action in ['sorting', 'searching']:
          data = get_items(searchinput, sortvar, sortcolumn)

        if action == 'cart':
            cart_id = request.form.get('userid')
            product_id = request.form.get('productid')

            c_data = (cart_id, product_id)
            print(f"[LOG] - Trying to add to cart with values: {c_data}")
            add_cart(c_data)
            return redirect('/shop')

        print(f"[LOG] - Action: {action}, Search: {searchinput}, Sort: {sortvar}, Sort Column: {sortcolumn}")
        
    return render_template("shop.html", items=data, role=role, user=user)

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    data = cat_description_get()

    role = session.get('role', None)  # None if not logged in
    if request.form.get('action') == 'login':
       return redirect('/login')
    if request.form.get('action') == 'shop':
       return redirect('/shop')
    # If not admin, don't show the table
    if role != 'admin':
      return render_template("shop.html")
    
    # This looks out for POST requests from modals
    if request.method == 'POST':
        # Find what action the modal was looking for, and execute the function for the action the modal stated below
        action = request.form.get("action")

        # If the modal was to edit an item
        if action == 'saveItemBtn':
            print("[LOG] - Processing POST request for editing an item")
            # Receiving the ID from the HTML form
            id = request.form.get('editID')
            # Specifying function i_name with values for each instance of ? in update_item(i_name)
            i_name = (
                request.form.get(f"editName{id}"),
                request.form.get(f"editCost{id}"),
	            request.form.get(f"editImage{id}"),
                request.form.get(f"editStock{id}"),
	            id
            )
            # Execute update_item(i_name)
            update_item(i_name)
            return redirect('/admin')
        
        if action == 'saveNameBtn':
            print("[LOG] - Processing POST request for editing a filter name")
            id = request.form.get('nameID')
            name = request.form.get(f'editName{id}')
            n_name = (name,id)
            update_name(n_name)
            return redirect('/admin')

        # If the modal was to add an item
        if action == 'add_item_form':
            print("[LOG] - Processing POST request to add an item")
            # Finding all values from the addItem___ inputs from the modals
            name = request.form.get("addItemName")
            cost = request.form.get("addItemCost")
            image = request.form.get("addItemImage")
            stock = request.form.get("addItemStock")
            # Specifying i_data with values for each instance of ? in add_item(i_data)
            i_data = (name,cost,image,stock)
            # Execute adding an item
            add_item(i_data)
            return redirect('/admin')
        
        if action == 'add_filter_form':
            print("[LOG] - Processing POST request to add a filter")
            id = request.form.get("addFilterID")
            name_id = request.form.get("addFilterNameID")
            f_data = (id, name_id)
            add_filter(f_data)
            return redirect('/admin')

        if action == 'add_filter_name_form':
            print("[LOG] - Processing POST request to add a filter name")
            n_data = request.form.get("addNameFilter")
            add_name(n_data)
            return redirect('/admin')

        if action == 'deleteFilterBtn':
            print("[LOG] - Processing POST request to delete a filter item")
            id = request.form.get("filterRemoveID")
            name_id = request.form.get("filterRemoveNameID")
            f_item = (id, name_id)
            remove_filter(f_item)
            return redirect('/admin')
        
        if action == 'deleteNameBtn':
            print("[LOG] - Processing POST request to delete a filter name")
            id = request.form.get("filterNameRemoveID")
            name_id = request.form.get("filterNameRemoveNameID")
            n_item = (id, name_id)
            remove_name(n_item)
            return redirect('/admin')

        if action == 'deleteCartBtn':
            print("[LOG] - Processing POST request to delete a cart item")
            product = request.form.get("cartRemoveProductID")
            id = request.form.get("cartRemoveID")
            c_item = (id, product)
            remove_cart(c_item)
            return redirect('/admin')

        # If the modal was to delete an item        
        if action == 'deleteItemBtn':
            print("[LOG] - Processing POST request to delete an item")
            # Find the id of the item to be deleted
            id = request.form.get("itemRemoveID")
            # ? = id
            i_item = (id)
            # Execute function to delete item
            remove_item(i_item)
            return redirect('/admin')
        
        if action == 'deletePurchsBtn':
            print("[LOG] - Processing POST request to delete a Purchase")
            purchaseid = request.form.get("purchsRemoveID")
            p_item = (purchaseid)
            remove_purchase(p_item)
            return redirect('/admin')
        
        if action == 'deletePurchsItemBtn':
            print("[LOG] - Processing POST request to delete a Purchase Item")
            purchaseid = request.form.get("purchsitemRemoveProductID")
            itemid = request.form.get("purchsitemRemoveItemID")
            p_item = (purchaseid, itemid)
            remove_purchase_item(p_item)
            return redirect('/admin')


    return render_template("index.html", items=data[0], filters=data[1], names=data[2], carts=data[3], purchs=data[4], purchsitems=data[5], role=role)

# App route for the login page, contains the login function.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      # Get the username and password from the front end
      username = request.form.get('username')
      password = request.form.get('password')

      print('[LOG] - Fetching username data')
      with sqlite3.connect('assets/shopped_data.db') as conn:
          c = conn.cursor()
          c.row_factory = sqlite3.Row
          
          # Read the username from the database, fetch only one row
          c.execute("SELECT * FROM tbl_users WHERE username = ?", (username,))
          user = c.fetchone()
          print('[LOG] - Attempting login for', {username})
          # If the username exists in the database:
          if user is not None:
            #  If the user's password corresponds to that user's password:
             if user['password'] == password:
                session['username'] = username
                session['role'] = user['role']
                session['id'] = user['id'] 
                # Redirect the user to the index page + send a flash message that they have logged in
                flash(f'Logged in successfully for {username}')
                return redirect("/home")
             else:
                # If password does not match:
                flash(f'Password invalid')
          else:
            #  If username does not match:
             flash(f'Username invalid')
  
    # Update username function test
    # print("[LOG] - Updated a username - rows changed: ", update_user('jamesdapro', 2))
   
    # Delete user function test
    # print("[LOG] - Deleted a user - rows changed: ", delete_user(2))
    return render_template("login.html")

@app.route('/account', methods=['GET', 'POST'])
def account():
    
    data = cat_description_get()

    role = session.get('role', None)  # None if not logged in
    user = session.get('id', None)
    if request.form.get('action') == 'login':
       return redirect('/login')
    if request.form.get('action') == 'admin':
       return redirect('/admin')
    if request.form.get('action') == 'account':
       return redirect('/account')
    
  # This looks out for POST requests from modals
    if request.method == 'POST':
        # Find what action the modal was looking for, and execute the function for the action the modal stated below
        action = request.form.get("action")

        if action == 'deleteCartBtn':
            print("[LOG] - Processing POST request to delete a cart item")
            product = request.form.get("cartRemoveProductID")
            id = request.form.get("cartRemoveID")
            c_item = (id, product)
            remove_cart(c_item)
            return redirect('/admin')
        
        if action == 'order':
            print("LOG - Processing POST request to place order")

            # Get user's cart
            usercart = [c for c in data[3] if c['userid'] == user]  # data[3] is carts

            # Calculate total
            total = 0
            for c in usercart:
                for i in data[0]:  # data[0] is items
                    if i['id'] == c['product']:
                        total += i['cost']

            # Add order
            add_order(user, usercart, total)

            # Redirect to refresh page and show empty cart
            return redirect('/account')

    usercart = [c for c in data[3] if c['userid'] == user]  # data[3] is carts
    total = 0
    for c in usercart:
        # Find the matching item
        for i in data[0]:  # data[0] is items
            if i['id'] == c['product']:
                total += i['cost']

    return render_template("account.html", items=data[0], carts=data[3], role=role, user=user, total=total)


if __name__ == "__main__":
  print("[LOG] - Fullstack Webpage - Initialising")
  # Initialise Debugger
  app.run(debug=True, port=5050);


