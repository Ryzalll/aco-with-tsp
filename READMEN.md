# Ant Colony Intelligence

Ant Colony Intelligence (ACI) adalah metode komputasi yang terinspirasi dari perilaku koloni semut dalam mencari jalur terpendek antara sarang dan sumber makanan. Algoritma ini banyak digunakan untuk menyelesaikan masalah optimasi, seperti Travelling Salesman Problem (TSP).

## Konsep Dasar

- **Pheromone**: Semut meninggalkan jejak feromon di jalur yang mereka lewati. Semakin banyak semut melewati jalur tersebut, semakin kuat jejak feromonnya.
- **Probabilitas Pemilihan Jalur**: Semut memilih jalur berdasarkan kekuatan feromon dan jarak, sehingga jalur terbaik akan semakin sering dipilih.
- **Evaporasi Feromon**: Feromon menguap seiring waktu, mencegah solusi lokal yang tidak optimal.

## Aplikasi

- Travelling Salesman Problem (TSP)
- Penjadwalan tugas
- Routing jaringan
- Optimasi logistik

## Referensi

- Dorigo, M., & Gambardella, L. M. (1997). Ant Colony System: A Cooperative Learning Approach to the Traveling Salesman Problem.
- [Wikipedia: Ant Colony Optimization Algorithms](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)

---
Proyek ini mengimplementasikan algoritma Ant Colony Optimization untuk menyelesaikan TSP.