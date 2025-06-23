# app.py
from flask import Flask, render_template, request, redirect, url_for
import math
import matplotlib.pyplot as plt
import numpy as np
import random
from tabulate import tabulate
import datetime
import secrets
import os

app = Flask(__name__)

# setting up directory for store files
PLOT_FOLDER = os.path.join(app.root_path, 'static', 'plots')
if not os.path.exists(PLOT_FOLDER):
    os.makedirs(PLOT_FOLDER)

    
def getDataPheromones(data):
  cities = sorted(list(set([k[0] for k in data.keys()])))

  # 2. Buat struktur data yang lebih mudah untuk dirender sebagai tabel
  # Kita akan membuat list of lists, atau list of dictionaries jika ingin lebih eksplisit
  # Untuk kasus ini, list of lists lebih sederhana
  table_data = []

  for row_city in cities:
      row = [row_city] # Mulai baris dengan nama kota baris
      for col_city in cities:
          # Cari nilai yang sesuai di dictionary asli
          # Perhatikan bahwa key di dictionary adalah tuple, misalnya ('Gresik', 'Surabaya')
          value = data.get((row_city, col_city), 'N/A') # Gunakan .get() untuk menghindari KeyError
          table_data.append(value) # Untuk menyimpan nilai ke dalam list, tetapi ini kurang cocok untuk format tabel
          row.append(f"{value:.5f}") # Format nilai float menjadi 5 desimal
      table_data.append(row)


  # Versi lebih baik untuk struktur data tabel:
  # Mengonversi dictionary menjadi dictionary of dictionaries untuk akses O(1)
  # Ini membuat pencarian nilai lebih efisien di template
  processed_data = {}
  for (from_city, to_city), value in data.items():
      if from_city not in processed_data:
          processed_data[from_city] = {}
      processed_data[from_city][to_city] = value
      
  return processed_data

def penguapan_pheromones(pheromones, rho):
    for key in pheromones:
        pheromones[key] = (1 - rho) * pheromones[key]
    return pheromones

def hitung_jarak(all_city, city_from, city_to):

  x = abs(all_city[city_from][0] - all_city[city_to][0])
  y = abs(all_city[city_from][1] - all_city[city_to][1])

  return math.sqrt(x**2 + y**2)

def visualize_city(intersections, streets):

    # Pisahkan koordinat X dan Y untuk scatter plot
    x_coords = [coord[0] for coord in intersections.values()]
    y_coords = [coord[1] for coord in intersections.values()]

    # Inisialisasi figure dan axes
    plt.figure(figsize=(10, 8))
    ax = plt.gca() # Get current axes

    # Gambar node (persimpangan) menggunakan scatter plot
    plt.scatter(x_coords, y_coords,
                s=500, # Ukuran titik
                color="skyblue",
                edgecolors="blue",
                linewidths=1.5,
                zorder=2) # zorder agar titik berada di atas garis

    # Gambar edge (jalur) menggunakan plot
    for street_start, street_end in streets:
        # Ambil koordinat awal dan akhir jalur
        start_x, start_y = intersections[street_start]
        end_x, end_y = intersections[street_end]

        # Gambar garis
        plt.plot([start_x, end_x], [start_y, end_y],
                 color="gray",
                 linewidth=2,
                 alpha=0.7,
                 zorder=1) # zorder agar garis berada di bawah titik

        length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)

        # Tentukan posisi tengah jalur untuk menempatkan teks panjang
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # Tambahkan teks panjang jalur
        plt.text(mid_x, mid_y, f"{length:.2f}",
                fontsize=8,
                color='darkgreen',
                ha='center',
                va='center',
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="darkgreen", lw=0.5, alpha=0.8))

    # Tambahkan label nama persimpangan dan koordinat
    for name, (x, y) in intersections.items():
        # Label nama
        plt.text(x, y + 0.15, name,
                 fontsize=10,
                 fontweight="bold",
                 ha='center',
                 va='bottom',
                 color="black")

        # Label koordinat
        coord_text = f"({x:.1f}, {y:.1f})"
        plt.text(x, y - 0.20, coord_text,
                 fontsize=8,
                 color='red',
                 ha='center',
                 va='top',
                 bbox=dict(boxstyle="round,pad=0.2", fc="yellow", ec="darkred", lw=0.5, alpha=0.6))

    # Atur tampilan plot
    plt.title("Visualisasi jarak Kota", size=16, color="darkgreen")
    plt.xlabel("Koordinat X")
    plt.ylabel("Koordinat Y")
    plt.grid(True, linestyle='--', alpha=0.6) # Tampilkan grid
    plt.axis('equal') # Pastikan skala sumbu X dan Y sama
    # plt.show()
    
    plot_filename = f"plot_kota{secrets.randbelow(10)}.png"
    plot_path = os.path.join(PLOT_FOLDER, plot_filename)
    
    plt.savefig(plot_path)
    plt.close()
    
    return plot_filename

def tampilkanDict(dictionary):
   table_data = []
   for key, value in dictionary.items():
       table_data.append([key, value])

   headers = ['Kunci', 'Nilai']
   print(tabulate(table_data, headers=headers, tablefmt="grid"))

def hitung_komulatif_rute(no_semut,semut_1,jalur_one_semut, priors, pheromones, kota):
  pilihan_jalur_semut_1 = {}
  total = 0

  for jalur in pheromones:
    if semut_1[-1] == jalur[0] and jalur[-1] not in semut_1 :
      pilihan_jalur_semut_1[jalur] = priors[jalur] * pheromones[jalur]
      total += pilihan_jalur_semut_1[jalur]

  prob_route = {}
  count = 1
  for jalur in pilihan_jalur_semut_1:
    prob_route[jalur] = priors[jalur] * pheromones[jalur] / total
    count+=1

  random_number = random.random()


  sum_prob = 0
  for jalur in prob_route:
    sum_prob += prob_route[jalur]

  sum_prob = 0

  for jalur in prob_route:
    sum_prob += prob_route[jalur]
    if random_number < sum_prob:
      semut_1.append(jalur[-1])
      break
  text = f"<p>Misalkan bilangan acak yang dibangkitkan adalah {random_number},maka rute yang dipilih adalah {semut_1[-1]}</p>"

  jalur_one_semut += hitung_jarak(kota,semut_1[-2],semut_1[-1])

  return semut_1, jalur_one_semut, text

# Update pheromones dengan jalur yang dilewati semut
def update_pheromones_with_del_fit(jalur_semut, delt_fitness, pheromones):
  for key in pheromones:
    if key[0] != key[1]:
      for i in range(len(jalur_semut)):
        for j in range(len(jalur_semut[i]) - 1):
          if jalur_semut[i][j:j+2] == list(key):
            pheromones[key] += delt_fitness[i]
    return pheromones


def aco(jumlah_iterasi, jumlah_semut, all_kota, jalur_kota,p, pheromones, kota):
  priors = {}
  all_pheromones = []
  text_rout = ''
  for jalur in jalur_kota:
    priors[jalur] = 0 if jalur_kota[jalur] == 0 else 1/jalur_kota[jalur]

  # all_kota

  jalur_hasil_akhir = None
  jalur_rangkaian_kota_akhir = None

  for i in range(jumlah_iterasi):
    text_rout += f'<div><p>Iterasi ke-{i+1}</p>'
    jalur_semut = []

    for i in range(jumlah_semut):
      tup = []
      tup.append(all_kota[random.randint(0, len(all_kota)-1)])
      jalur_semut.append((tup))

    delt_fitness = []

    for i in range(len(jalur_semut)):
      text_rout += f'<p>Kota awal semut ke-{i+1} adalah {jalur_semut[i][0]} </p>'
      one_ant = jalur_semut[i]
      jalur_one_semut = 0
      for j in range(len(all_kota)-1):
        one_ant,jalur_one_semut,text_temp  = hitung_komulatif_rute(i+1, one_ant, jalur_one_semut, priors, pheromones, kota)
        # one_ant,jalur_one_semut = hitung_komulatif_rute_with_latex(i+1,one_ant, jalur_one_semut)
        text_rout += text_temp
        
      for one_kota in all_kota:
        if one_kota not in one_ant:
          one_ant.append(one_kota)

      delt_fitness.append(1/jalur_one_semut)

      if jalur_hasil_akhir == None:
        jalur_hasil_akhir = jalur_one_semut
        jalur_rangkaian_kota_akhir = one_ant
      else:
        if jalur_one_semut < jalur_hasil_akhir:
          jalur_hasil_akhir = jalur_one_semut
          jalur_rangkaian_kota_akhir = one_ant
      jalur_semut[i] = one_ant

      # print("Jalur semut ke",i+1,one_ant)
      # print("Jarak tempuh semut ke",i+1,jalur_one_semut)
      # print("Delta fitness semut ke",i+1,delt_fitness[i])
      # print('\n---\n')
      
      text_rout += ("<p>Jalur semut ke-" + str(i+1) +' = '+ str(one_ant)+ '</p>')
      text_rout += ("<p>Jarak tempuh semut ke-"+ str(i+1) +' = '+ str(jalur_one_semut)+ '</p>')
      text_rout += ("<p>Delta fitness semut ke-"+ str(i+1) +' = '+ str(delt_fitness[i])+ '</p>')
      
    pheromones = update_pheromones_with_del_fit(jalur_semut, delt_fitness, pheromones)
    pheromones = penguapan_pheromones(pheromones, p)
    
    all_pheromones.append(getDataPheromones(pheromones))
    
    text_rout += '</div>'

  return jalur_hasil_akhir, jalur_rangkaian_kota_akhir, pheromones, text_rout, all_pheromones

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
    
    kota = {}
    jumlah_semut = int(request.form.get('jumlah_semut'))
    jumlah_iterasi = int(request.form.get('jumlah_iterasi'))
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
                kota[nama_kota] = (koor_x, koor_y)
            except ValueError:
                print(f"DEBUG: Skipping invalid coordinates for {nama_kota_key}: x='{koor_x_str}', y='{koor_y_str}'")
                # Anda bisa memilih untuk mengabaikan atau memberi pesan error
        else:
            print(f"DEBUG: Incomplete data for kota-{i}: Nama={nama_kota}, X={koor_x_str}, Y={koor_y_str}")
        i += 1
    print("Parsed data_kota:", kota)  # DEBUG: Print data setelah diparsing
    
    # Main Program
    jalur_kota = {}

    for kota_from in kota:
        for kota_to in kota:
            jalur = (kota_from,kota_to)
            jalur_kota[jalur] = hitung_jarak(kota,kota_from,kota_to)

    file_name = visualize_city(kota,[x for x in jalur_kota])

    # Inisialisasi Pheromones
    pheromones = {}

    for jalur in jalur_kota:
        pheromones[jalur] = 0 if jalur_kota[jalur] == 0 else 0.01

    # tampilkanDict(pheromones)

    # Inisialisasi Penguapan pheromones
    p = 50/100

    all_kota = tuple(list(kota.keys()))

    print(aco(jumlah_iterasi, jumlah_semut, all_kota,jalur_kota, p,pheromones, kota))
    jalur_hasil_akhir, jalur_rangkaian_kota_akhir, pheromones,text_rout, all_pheromones = aco(jumlah_iterasi, jumlah_semut, all_kota,jalur_kota, p, pheromones, kota)
    
    jalur_hasil_akhir = round(jalur_hasil_akhir, 3)
    
    str_jalur = ''
    
    for i in jalur_rangkaian_kota_akhir:
        str_jalur += str(i) + ' -> '
    
    str_jalur = str_jalur[:len(str_jalur)-4]
    
    if kota:
        return render_template('results.html', 
                               jarak=jalur_hasil_akhir, 
                               jalur=str_jalur,
                               file_url = url_for('static',filename = f'plots/{file_name}'),
                               text_html = text_rout,
                               semua_pheromones = all_pheromones)  # Pastikan ini ada!
    else:
        print("DEBUG: No valid city data found, redirecting to index.")
        return redirect(url_for('index')) # Hapus ini sementara untuk debugging


@app.route('/delete-plot', methods=['POST'])
def delete_plot():
    data = request.get_json()
    filename = data.get('filename')
    if filename:
        file_path = os.path.join(PLOT_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {'success': True}
    return {'success': False}, 400


if __name__ == '__main__':
    app.run(debug=True)