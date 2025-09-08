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
def get_items(columns, searchinput, sortvar, sortcolumn):
  # Establish connection to the database and grab the cursor
  conn = get_db_connection()
  cur = conn.cursor()
  # Rewrite the string list to remove the apostrophes so that it can work in the SQL function
  sqlcolumns = ", ".join(columns)
  print("[LOG] - Attempting to execute SQL function")
    # Each function is put into place in the SQL code
  sql = f"""
  SELECT {sqlcolumns} FROM tbl_items
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
  print(f"[LOG] - Columns selected: {sqlcolumns}.")
  print("---------------------------------------------------------------")
  conn.close()

  return changed_table;

# Function to prove DELETE process
def delete_user(user_id):
   conn = get_db_connection()
  #  Deletes from SQL in this order to abide by referential integrity
   sql1 = '''DELETE FROM tbl_purchs_items WHERE purchase_id = ?'''
   sql2 = '''DELETE FROM tbl_purchs WHERE user = ?'''
   sql3 = '''DELETE FROM tbl_users WHERE id = ?'''
   conn.execute(sql1, (user_id,))
   conn.execute(sql2, (user_id,))
   c = conn.execute(sql3, (user_id,))
   conn.commit()
  #  Return how many rows were affected so that we can check if anything was changed.
   return c.rowcount

# Function to prove UPDATE process
def update_user(name,id):
   conn = get_db_connection()
   sql = '''UPDATE tbl_users SET username = ? WHERE id = ?'''
  #  Update someones username according to their ID
   c = conn.execute(sql, (name, id))
   conn.commit()
  #  Return the number of rows affected to prove this function works
   return c.rowcount


app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Encrypts the data in the session, this is irrelevant so there is a placeholder for now
app.config['SECRET_KEY'] = 'secret_key_placeholder'

# When there is no set @app.route, automatically route to /login
@app.route("/",methods=['GET', 'POST'])
def default():
   print("[LOG] - Redirecting to login")
   return redirect("/login")

# Index app route from last year - irrelevant for this internal
@app.route('/index', methods=['GET', 'POST'])
def index():
    role = session.get('role', None)  # None if not logged in
    if request.form.get('action') == 'login':
       return redirect('/login')
    # If not admin, don't show the table
    if role != 'admin':
        return render_template("index.html", columns=[], items=[], role=role)
    # Default values for when the page initially loads
    sortcolumn = 'id'
    sortvar = 'ASC'
    searchinput = ''
    columns = ['id', 'name', 'cost', 'image', 'stock']
    # Execute this function when the page first loads without an action so that there is a table
    data = get_items(columns, searchinput, sortvar, sortcolumn)

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
        # Get the columns in a list
        columns = request.form.getlist("columns")

        # Ensure columns aren't empty. If they are, restore the default value
        if not columns:
            print(f"[LOG] - Columns are set to all off; preventing blank table")
            columns = ['id', 'name', 'cost', 'image', 'stock']

        # If the user decides to hit the reset button:
        if action == 'reset':
            print("[LOG] - Restoring to default settings.")
            # All values are restored to the aforementioned default values
            sortcolumn = 'id'
            sortvar = 'ASC'
            searchinput = ''
            columns = ['id', 'name', 'cost', 'image', 'stock']
            data = get_items(columns, searchinput, sortvar, sortcolumn)

        # For all other action types, execute function get_items().
        elif action in ['filtering', 'sorting', 'searching']:
            data = get_items(columns, searchinput, sortvar, sortcolumn)

        print(f"[LOG] - Action: {action}, Search: {searchinput}, Sort: {sortvar}, Sort Column: {sortcolumn}, Columns: {columns}")

    return render_template("shop.html", items=data, columns=columns, role=role)

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
                # Redirect the user to the index page + send a flash message that they have logged in
                flash(f'Logged in successfully for {username}')
                return redirect("/index")
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

if __name__ == "__main__":
  print("[LOG] - Login Page - Initialising")
  # Initialise Debugger
  app.run(debug=True, port=5050);