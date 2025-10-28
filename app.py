from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'replace-with-secure-secret')


# --- MySQL configuration: update these values or use environment variables ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'portfolio_db'


mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cur.fetchall()
    cur.close()
    return render_template('index.html', projects=projects)
@app.route('/project/<int:project_id>')
def project_detail(project_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM projects WHERE id=%s', (project_id,))
    project = cur.fetchone()
    cur.close()
    if not project:
    return redirect(url_for('index'))
    return render_template('project.html', project=project)