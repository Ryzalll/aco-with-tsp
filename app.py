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
    print("Form Data:", request.form)  # DEBUG: Print semua data form
    
    data_kota = []
    jumlah_semut = request.form.get('jumlah_semut')
    jumlah_iterasi = request.form.get('jumlah_iterasi')
    i = 0
    while True:
        nama_kota_key = f'kota-{i}'
        koor_x_key = f'x-kota-{i}'
        koor_y_key = f'y-kota-{i}'

        nama_kota = request.form.get(nama_kota_key)
        koor_x_str = request.form.get(koor_x_key)  # Ambil sebagai string dulu
        koor_y_str = request.form.get(koor_y_key)  # Ambil sebagai string dulu
        
        if nama_kota is None:
            break
        if nama_kota and koor_x_str is not None and koor_y_str is not None:
            try:
                # Konversi ke float, tangani jika bukan angka
                koor_x = float(koor_x_str)
                koor_y = float(koor_y_str)
                data_kota.append({
                    'nama': nama_kota,
                    'x': koor_x,
                    'y': koor_y
                })
            except ValueError:
                print(f"DEBUG: Skipping invalid coordinates for {nama_kota_key}: x='{koor_x_str}', y='{koor_y_str}'")
                # Anda bisa memilih untuk mengabaikan atau memberi pesan error
        else:
            print(f"DEBUG: Incomplete data for kota-{i}: Nama={nama_kota}, X={koor_x_str}, Y={koor_y_str}")
        i += 1
    print("Parsed data_kota:", data_kota)  # DEBUG: Print data setelah diparsing
    
    if data_kota:
        return render_template('results.html', data_kota=data_kota, jumlah_semut=jumlah_semut, jumlah_iterasi=jumlah_iterasi)  # Pastikan ini ada!
    else:
        print("DEBUG: No valid city data found, redirecting to index.")
        return redirect(url_for('index')) # Hapus ini sementara untuk debugging

if __name__ == '__main__':
    app.run(debug=True)