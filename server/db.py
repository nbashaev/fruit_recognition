import os
import sqlite3
from flask import g


DB_PATH = os.path.join('db', 'labels.db')


class DB_Wrapper:
	def __init__(self, db_path):
		g.conn = sqlite3.connect(db_path)
		g.c = g.conn.cursor()
		g.c.execute('CREATE TABLE IF NOT EXISTS processed_paths(path TEXT)')
		g.c.execute('CREATE TABLE IF NOT EXISTS labels(path TEXT, class TEXT, xmin REAL,  ymin REAL,  xmax REAL,  ymax REAL)')
	
	def add_record(self, img_path, labels):
		g.c.execute('INSERT INTO processed_paths VALUES (?)', [img_path])
	
		for label in labels:
			g.c.execute('INSERT INTO labels VALUES (?, ?, ?, ?, ?, ?)',
				[img_path, label['name'], label['xMin'], label['yMin'], label['xMax'], label['yMax']]
			)
		
		g.conn.commit()
	
	def get_all_paths(self):
		g.c.execute('SELECT * FROM processed_paths')
		return [path_tuple[0] for path_tuple in g.c.fetchall()]
	
	def get_group_by_path(self, img_path):
		g.c.execute('SELECT * FROM labels WHERE path=?', [img_path])
		
		return [{
			'class': row[1],
			'xmin': row[2],
			'ymin': row[3],
			'xmax': row[4],
			'ymax': row[5],
		} for row in g.c.fetchall()]


def get_db_wrapper():
	if 'db' not in g:
		g.db = DB_Wrapper(DB_PATH)
	
	return g.db