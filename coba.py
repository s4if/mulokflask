from flask import Flask, render_template
import sqlite3

# Nama Database
DATABASE = 'app.db'

app = Flask(__name__)

@app.route('/')
def home():
    return "Halaman Home"

@app.route('/salam')
def salam():
    return "Assalamu'alaikum"

@app.route('/salam/<string:nama>')
def salam2(nama):
    return "Assalamu\'alaikum, yaa "+nama

@app.route('/tambah/<int:a>/<int:b>')
def tambah(a, b):
    c = a+b
    return f'{a} + {b} = {c}'

@app.route('/template')
def template():
    return render_template(
        'coba.html',
        judul="halaman bertemplate",
        isi="Ini adalah template!!"
        )

pages = [
    {'judul':'Halaman 1', 'isi':'isi halaman 1'},
    {'judul':'Halaman 2', 'isi':'isi halaman 2'},
    {'judul':'Halaman 3', 'isi':'isi halaman 3'}
]
pages.append({'judul':'Susahnya buat puisi', 'isi':'''
Ini susahnya membuat puisi<br>
Kata-Kata berlarian di dalam hati<br>
Ganas Terjang Sana Sini<br>
Dapat satu, hilang seribu<br>
Dapat Dua ditabrak lari<br>
Hilang Sudah Sejuta Puisi<br>
'''})

@app.route('/blog/<int:id>')
def blog(id):
    try:
        page = pages[id-1]
        return render_template(
            'coba.html',
            judul=page['judul'],
            isi=page['isi']
        )
    except IndexError:
        return "Mohon maaf, halaman tidak ditemukan!", 404
    

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def close_db(conn):
    conn.close()

@app.cli.command('init-db')
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs(
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   judul TEXT NOT NULL,
                   isi TEXT NOT NULL);
        ''')
    conn.commit()
    close_db(conn)
    print('Database telah dibuat')

@app.cli.command('import-data')
def import_data():
    conn = get_db()
    cursor = conn.cursor() # sambungan
    for page in pages:
        cursor.execute('''
            INSERT INTO blogs(judul,isi) VALUES(?,?);
        ''', (page['judul'], page['isi']))
    conn.commit()
    close_db(conn)
    print('Data Telah DIIMPORT')

@app.route('/new_blog/<int:id>')
def new_blog(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT judul, isi FROM blogs WHERE id=? ;
    ''', (id,))
    blog = cursor.fetchone()
    if blog :
        return render_template(
            'coba.html',
            judul=blog[0],
            isi=blog[1]
        )
    else : return 'Halaman tidak ditemukan!', 404