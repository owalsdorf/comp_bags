import sqlite3;

# Creates connection to the database
with sqlite3.connect("assets/shopped_data.db") as conn:
	# Run our sql to initialise the database, using with_resources pattern
	with open('setup/bags.sql') as f:
		conn.executescript(f.read())

	# Grab cursor
	cur = conn.cursor();
	all_items = cur.execute('SELECT * FROM tbl_items').fetchall()
	print(all_items)

	print("[LOG] - Database Initialised")

	# Save changes to database
	conn.commit();