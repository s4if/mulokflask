from flask import Flask, render_template

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