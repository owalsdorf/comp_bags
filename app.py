from flask import Flask, render_template, request, redirect
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
      logging.debug('get_db_connection()')
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

app = Flask(__name__, static_url_path='/assets', static_folder='assets');

# Allows for a GET request if needed - but not used
@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template("login.html")


if __name__ == "__main__":
  print("[LOG] - Search engine - Initialising")
  # Initialise Debugger
  app.run(debug=True, port=5050);