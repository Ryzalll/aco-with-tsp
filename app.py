# app.py
from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Rute untuk menampilkan formulir input nama
@app.route('/', methods=['GET'])
def index():
    # Ini adalah halaman utama dengan formulir
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%A, %d %B %Y")
    return render_template('index.html', current_time=current_time, current_date=current_date)

# Rute untuk memproses data formulir
@app.route('/results', methods=['POST'])
def results():
    # Metode POST berarti formulir telah dikirimkan
    user_name = request.form.get('user_name') # Mengambil nilai dari input 'user_name'

    if user_name:
        # Jika nama ada, tampilkan halaman sambutan personal
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%A, %d %B %Y")
        return render_template('results.html',
                               name=user_name,
                               current_time=current_time,
                               current_date=current_date)
    else:
        # Jika nama kosong, arahkan kembali ke halaman utama atau tampilkan pesan error
        return redirect(url_for('index')) # Kembali ke halaman utama

if __name__ == '__main__':
    app.run(debug=True)