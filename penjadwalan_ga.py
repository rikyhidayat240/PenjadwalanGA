import random
import copy
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sistem Penjadwalan", layout="wide")

class AlgoritmaGenetika:
    def __init__(self, data_sistem, ukuran_populasi=30, crossover_rate=0.7, mutation_rate=0.04):
        self.data = data_sistem
        self.ukuran_populasi = ukuran_populasi
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.slot_per_hari = {}
        
        for slot in self.data['slot_waktu']:
            hari = slot['hari']
            if hari not in self.slot_per_hari:
                self.slot_per_hari[hari] = []
            self.slot_per_hari[hari].append(slot)
            
    def buat_kromosom_acak(self):
        kromosom = []
        for tugas in self.data['beban_mengajar']:
            sks = tugas['sks']
            ruang_acak = random.choice(self.data['ruangan'])
            hari_acak = random.choice(list(self.slot_per_hari.keys()))
            slot_hari_ini = self.slot_per_hari[hari_acak]
            
            max_start_idx = len(slot_hari_ini) - sks
            if max_start_idx < 0:
                start_idx = 0
                sks = len(slot_hari_ini)
            else:
                start_idx = random.randint(0, max_start_idx)
            
            slot_terpilih = slot_hari_ini[start_idx : start_idx + sks]
            id_slot_terpilih = [s['id_slot'] for s in slot_terpilih]
            
            gen = {
                'kode': tugas.get('kode', '-'),
                'matkul': tugas['matkul'],
                'kelas': tugas['kelas'],
                'semester': tugas.get('semester', '-'),
                'dosen': tugas['dosen'],             
                'dosen_list': tugas['dosen_list'],   
                'sks': sks,
                'ruang': ruang_acak,
                'hari': hari_acak,
                'jam_mulai': slot_terpilih[0]['jam_mulai'],
                'jam_selesai': slot_terpilih[-1]['jam_selesai'],
                'id_slot': id_slot_terpilih
            }
            kromosom.append(gen)
        return kromosom
    
    def inisialisasi_populasi(self):
        return [self.buat_kromosom_acak() for _ in range(self.ukuran_populasi)]

    def hitung_fitness(self, kromosom):
        CD, CK, CR, CH = 0, 0, 0, 0
        pemakaian_slot = {}
        
        for gen in kromosom:
            dosen_list = gen['dosen_list']
            kelas = gen['kelas']
            ruang = gen['ruang']
            hari = gen['hari']
            
            for d in dosen_list:
                if hari in self.data['dosen'].get(d, []):
                    CH += 1
                
            for id_slot in gen['id_slot']:
                if id_slot not in pemakaian_slot:
                    pemakaian_slot[id_slot] = {'dosen': [], 'kelas': [], 'ruang': []}
                slot_data = pemakaian_slot[id_slot]
                
                for d in dosen_list:
                    if d in slot_data['dosen']: CD += 1
                    slot_data['dosen'].append(d)
                
                if kelas in slot_data['kelas']: CK += 1
                if ruang in slot_data['ruang']: CR += 1
                
                slot_data['kelas'].append(kelas)
                slot_data['ruang'].append(ruang)
                
        total_konflik = CD + CK + CR + CH
        return 1.0 / (1.0 + total_konflik), total_konflik

    def seleksi_turnamen(self, populasi, fitnesses):
        peserta = random.sample(list(zip(populasi, fitnesses)), 3)
        peserta.sort(key=lambda x: x[1], reverse=True)
        return peserta[0][0]

    def crossover(self, induk1, induk2):
        titik_potong = random.randint(0, len(induk1)-1)
        anak = induk1[:titik_potong] + induk2[titik_potong:]
        return anak

    def mutasi(self, kromosom, peluang):
        if random.random() < peluang:
            idx = random.randint(0, len(kromosom)-1)
            
            if random.random() < 0.5:
                kromosom[idx]['ruang'] = random.choice(self.data['ruangan'])
            else:
                sks = kromosom[idx]['sks']
                hari_acak = random.choice(list(self.slot_per_hari.keys()))
                slot_hari_ini = self.slot_per_hari[hari_acak]
                
                max_start_idx = len(slot_hari_ini) - sks
                if max_start_idx >= 0:
                    start_idx = random.randint(0, max_start_idx)
                    slot_terpilih = slot_hari_ini[start_idx : start_idx + sks]
                    
                    kromosom[idx]['hari'] = hari_acak
                    kromosom[idx]['jam_mulai'] = slot_terpilih[0]['jam_mulai']
                    kromosom[idx]['jam_selesai'] = slot_terpilih[-1]['jam_selesai']
                    kromosom[idx]['id_slot'] = [s['id_slot'] for s in slot_terpilih]
                    
        return kromosom

    def evolusi(self, populasi, generasi=100, progress_bar=None, status_text=None):
        for gen in range(generasi):
            fitnesses = [self.hitung_fitness(k)[0] for k in populasi]
            populasi_baru = []
            
            terbaik_idx = fitnesses.index(max(fitnesses))
            populasi_baru.append(copy.deepcopy(populasi[terbaik_idx]))
            
            while len(populasi_baru) < self.ukuran_populasi:
                i1 = self.seleksi_turnamen(populasi, fitnesses)
                i2 = self.seleksi_turnamen(populasi, fitnesses)
                
                if random.random() < self.crossover_rate:
                    anak = self.crossover(i1, i2)
                else:
                    anak = copy.deepcopy(i1)
                    
                anak = self.mutasi(anak, peluang=self.mutation_rate)
                populasi_baru.append(anak)
            populasi = populasi_baru
            
            if progress_bar and status_text and gen % 10 == 0:
                progress_bar.progress(gen / generasi)
                status_text.write(f"🧬 Sedang Evolusi... Generasi: {gen}/{generasi} | Fitness Terbaik Sementara: {max(fitnesses):.4f}")
                
        if progress_bar: progress_bar.progress(1.0)
        return populasi

    def simpan_ke_excel(self, kromosom, nama_file="jadwal_terbaik.xlsx"):
        data_tabel_raw = []
        for gen in kromosom:
            data_tabel_raw.append({
                'Hari': gen['hari'],
                'Waktu': f"{gen['jam_mulai']} - {gen['jam_selesai']}",
                'Kode MK': gen['kode'],
                'Mata Kuliah': gen['matkul'],
                'Kelas': gen['kelas'],
                'Semester': gen['semester'],
                'SKS': gen['sks'],
                'Dosen Pengampu': gen['dosen'],
                'Ruangan': gen['ruang']
            })
            
        df_raw = pd.DataFrame(data_tabel_raw)
        hari_map = {'Senin': 1, 'Selasa': 2, 'Rabu': 3, 'Kamis': 4, 'Jumat': 5, 'Sabtu': 6, 'Minggu': 7}
        df_raw['Urutan_Hari'] = df_raw['Hari'].map(hari_map)
        df_raw = df_raw.sort_values(by=['Urutan_Hari', 'Waktu']).drop('Urutan_Hari', axis=1).reset_index(drop=True)
        
        ruangan_list = self.data['ruangan']
        hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        
        baris_waktu = []
        grid_data = []
        
        for hari in hari_list:
            if hari not in self.slot_per_hari: continue
                
            baris_waktu.append(f"====== {hari.upper()} ======")
            grid_data.append([""] * len(ruangan_list))
            
            for slot in self.slot_per_hari[hari]:
                waktu_str = f"{slot['jam_mulai']} sd {slot['jam_selesai']}"
                baris_waktu.append(waktu_str)
                
                row_data = []
                for ruang in ruangan_list:
                    teks_sel = ""
                    for gen in kromosom:
                        if gen['hari'] == hari and gen['ruang'] == ruang:
                            if slot['id_slot'] in gen['id_slot']:
                                teks_sel = f"{gen['matkul']} ({gen['kelas']}) - {gen['dosen']}"
                                break
                    row_data.append(teks_sel)
                grid_data.append(row_data)
                
        df_grid = pd.DataFrame(grid_data, columns=ruangan_list, index=baris_waktu)
        df_grid.index.name = 'WAKTU'
        
        with pd.ExcelWriter(nama_file, engine='openpyxl') as writer:
            df_grid.to_excel(writer, sheet_name='Jadwal_Matriks')
            df_raw.to_excel(writer, sheet_name='Jadwal_Datar', index=False)
            
        return df_grid, df_raw


if __name__ == "__main__":
    from data_parser import muat_data_excel

    st.markdown("""
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Sistem Penjadwalan Otomatis")
    st.write("Unggah file data_jadwal.xlsx Anda untuk memulai pencarian jadwal tanpa bentrok.")

    uploaded_file = st.file_uploader("Pilih File Data Master (Excel)", type=['xlsx'])

    if uploaded_file is not None:
        temp_filename = "temp_data_jadwal.xlsx"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        data = muat_data_excel(temp_filename)
        
        if data:
            st.write("Data berhasil dimuat. Siap diproses.")
            
            st.write("---")
            st.subheader("Filter Semester")
            semua_semester = sorted(list(set([item['semester'] for item in data['beban_mengajar']])))
            
            selected_semesters = []
            if semua_semester:
                cols = st.columns(min(len(semua_semester), 8))
                for i, sem in enumerate(semua_semester):
                    with cols[i % 8]:
                        if st.checkbox(f"Semester {sem}", value=True):
                            selected_semesters.append(sem)
            
            if not selected_semesters:
                st.warning("Silakan centang minimal 1 semester untuk dilanjutkan.")
                st.stop()
                
            data['beban_mengajar'] = [item for item in data['beban_mengajar'] if item['semester'] in selected_semesters]
            
            st.write("---")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Durasi SKS", f"{data['info_sistem']['durasi_sks']} Menit")
            col2.metric("Total Dosen", f"{len(data['dosen'])} Orang")
            col3.metric("Total Ruang", f"{len(data['ruangan'])} Ruangan")
            col4.metric("Beban Kelas (Difilter)", f"{len(data['beban_mengajar'])} Kelas")
            
            st.write("---")
            
            st.subheader("Konfigurasi Algoritma")
            
            col_set1, col_set2, col_set3 = st.columns(3)
            with col_set1:
                maksimal_percobaan = st.number_input("Batas Auto-Restart", min_value=1, max_value=50, value=3)
            with col_set2:
                ukuran_pop = st.number_input("Ukuran Populasi", min_value=10, max_value=500, value=150)
            with col_set3:
                jumlah_generasi = st.number_input("Jumlah Generasi", min_value=100, max_value=5000, value=1000)

            col_set4, col_set5, col_btn = st.columns(3)
            with col_set4:
                input_crossover = st.number_input("Crossover Rate", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
            with col_set5:
                input_mutasi = st.number_input("Mutation Rate (%)", min_value=0.0, max_value=100.0, value=4.0, step=1.0) / 100.0
            
            with col_btn:
                st.write("")
                mulai_proses = st.button("Buat Jadwal Sekarang", use_container_width=True)
                
            if mulai_proses:
                jadwal_terbaik_global = None
                fitness_terbaik_global = 0
                total_konflik_terbaik_global = float('inf')
                
                percobaan = 1
                
                while percobaan <= maksimal_percobaan:
                    st.write(f"#### Menjalankan Percobaan {percobaan} dari {maksimal_percobaan}")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    ga = AlgoritmaGenetika(
                        data_sistem=data, 
                        ukuran_populasi=ukuran_pop, 
                        crossover_rate=input_crossover, 
                        mutation_rate=input_mutasi
                    )
                    populasi = ga.inisialisasi_populasi()
                    
                    populasi_akhir = ga.evolusi(populasi, generasi=jumlah_generasi, progress_bar=progress_bar, status_text=status_text)
                    
                    fitnesses = [ga.hitung_fitness(k)[0] for k in populasi_akhir]
                    terbaik_idx = fitnesses.index(max(fitnesses))
                    jadwal_terbaik_lokal = populasi_akhir[terbaik_idx]
                    nilai_terbaik_lokal, total_konflik_lokal = ga.hitung_fitness(jadwal_terbaik_lokal)
                    
                    status_text.write(f"Percobaan {percobaan} Selesai! Fitness: {nilai_terbaik_lokal:.4f} | Sisa Bentrok: {total_konflik_lokal}")
                    
                    if nilai_terbaik_lokal > fitness_terbaik_global:
                        fitness_terbaik_global = nilai_terbaik_lokal
                        jadwal_terbaik_global = copy.deepcopy(jadwal_terbaik_lokal)
                        total_konflik_terbaik_global = total_konflik_lokal
                        
                    if fitness_terbaik_global == 1.0:
                        break
                    else:
                        percobaan += 1
                
                st.write("---")
                st.subheader("Hasil Pencarian Akhir")
                if fitness_terbaik_global == 1.0:
                    st.write("**Jadwal sempurna berhasil ditemukan.** (Nilai Fitness: 1.0 | 0 Tabrakan)")
                else:
                    st.write(f"Jadwal paling optimal (Fitness {fitness_terbaik_global:.4f}), tersisa {total_konflik_terbaik_global} bentrok.")
                
                df_grid, df_raw = ga.simpan_ke_excel(jadwal_terbaik_global, "jadwal_terbaik.xlsx")
                
                st.write("### Pratinjau Jadwal (Format Matriks)")
                st.dataframe(df_grid, use_container_width=True, height=600)
                
                with open("jadwal_terbaik.xlsx", "rb") as file:
                    st.download_button(
                        label="Unduh File Excel (Matriks & Data Lengkap)",
                        data=file,
                        file_name="Jadwal_Optimal_Matriks.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )