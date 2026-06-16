import pandas as pd
from datetime import datetime, timedelta

def buat_slot_waktu(jam_mulai_str, jam_selesai_str, durasi_menit):
    """
    Fungsi ini bertugas memotong-motong jam operasional kampus 
    menjadi blok/slot waktu baku (misalnya per 50 menit).
    """
    jam_mulai_str = str(jam_mulai_str)[:5]
    jam_selesai_str = str(jam_selesai_str)[:5]
    
    fmt = "%H:%M"
    start_time = datetime.strptime(jam_mulai_str, fmt)
    end_time = datetime.strptime(jam_selesai_str, fmt)
    
    hari_kerja = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    daftar_slot = []
    
    for hari in hari_kerja:
        curr_time = start_time
        slot_index = 1
        
        while curr_time + timedelta(minutes=durasi_menit) <= end_time:
            next_time = curr_time + timedelta(minutes=durasi_menit)
            daftar_slot.append({
                'hari': hari,
                'jam_mulai': curr_time.strftime(fmt),
                'jam_selesai': next_time.strftime(fmt),
                'id_slot': f"{hari}_{slot_index}"
            })
            curr_time = next_time
            slot_index += 1
            
    return daftar_slot

def muat_data_excel(filepath='data_jadwal.xlsx'):
    """
    Membaca file Excel dan merapikannya ke format siap proses.
    Otomatis memfilter kelas MBKM dan mendukung merged cells tim dosen.
    """
    try:
        xls = pd.read_excel(filepath, sheet_name=None)
        nama_sheets = list(xls.keys())
    except FileNotFoundError:
        print(f"Error: File '{filepath}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"Error membaca Excel: {e}")
        return None

    # 1. PARAMETER GLOBAL
    df_param = xls[nama_sheets[0]]
    param_dict = dict(zip(df_param.iloc[:, 0], df_param.iloc[:, 1]))
    
    jam_mulai = param_dict['Jam Mulai Operasional']
    jam_selesai = param_dict['Jam Selesai Operasional']
    durasi_sks = int(param_dict['Durasi 1 SKS'])
    
    slot_waktu = buat_slot_waktu(jam_mulai, jam_selesai, durasi_sks)

    # 2. DATA RUANGAN
    df_ruang = xls[nama_sheets[1]]
    ruangan = df_ruang.iloc[:, 0].dropna().tolist() 

    # 3. DATA DOSEN
    df_dosen = xls[nama_sheets[2]]
    dosen_libur = {}
    
    for _, row in df_dosen.iterrows():
        nama = str(row.iloc[0]).strip()
        libur_raw = row.iloc[1]
        
        if pd.notna(libur_raw):
            libur_list = [h.strip() for h in str(libur_raw).split(',')]
        else:
            libur_list = []
            
        dosen_libur[nama] = libur_list

    # 4. DATA MATA KULIAH (Penyesuaian Index Kolom Baru)
    df_matkul = xls[nama_sheets[3]]
    beban_mengajar = []
    
    skip_current_class = False 
    
    for _, row in df_matkul.iterrows():
        # Kolom 0 sekarang adalah "Kurikulum", Kolom 1 adalah "Kode Matkul"
        kode_raw = row.iloc[1] 
        
        # Skenario 1: Ini adalah baris Matkul baru
        if pd.notna(kode_raw) and str(kode_raw).strip() != "":
            kode_matkul = str(kode_raw).strip()
            nama_matkul_raw = str(row.iloc[2]).strip() # Kolom 2 = Nama
            
            if "MBKM" in nama_matkul_raw.upper():
                skip_current_class = True
                continue
            
            skip_current_class = False
            
            if "(" in nama_matkul_raw and ")" in nama_matkul_raw:
                matkul = nama_matkul_raw.split("(")[0].strip()
                kelas = nama_matkul_raw.split("(")[1].replace(")", "").strip()
            else:
                matkul = nama_matkul_raw
                kelas = "-" 
                
            # Pastikan isinya angka dengan aman (Kolom 3 = Semester, Kolom 4 = SKS)
            semester_val = str(row.iloc[3]).strip()
            sks_val = str(row.iloc[4]).strip()
            
            semester = int(float(semester_val)) if semester_val.replace('.', '', 1).isdigit() else 0
            sks = int(float(sks_val)) if sks_val.replace('.', '', 1).isdigit() else 0
            
            # Kolom 5 = Nama Dosen
            dosen_raw = str(row.iloc[5]).strip()
            dosen = dosen_raw.split(":")[-1].strip() if ":" in dosen_raw else dosen_raw
            
            beban_mengajar.append({
                'kode': kode_matkul,
                'matkul': matkul,
                'kelas': kelas,
                'semester': semester,
                'sks': sks,
                'dosen_list': [dosen] if dosen and dosen != "nan" else [],
                'dosen': dosen if dosen and dosen != "nan" else ""
            })
            
        # Skenario 2: Ini adalah baris anggota dosen (Sel Excel di-merge)
        else:
            if skip_current_class:
                continue
                
            # Kolom 5 = Nama Dosen Anggota
            dosen_raw = str(row.iloc[5]).strip()
            
            if pd.notna(row.iloc[5]) and dosen_raw != "" and dosen_raw != "nan":
                dosen = dosen_raw.split(":")[-1].strip() if ":" in dosen_raw else dosen_raw
                
                if len(beban_mengajar) > 0 and dosen:
                    beban_mengajar[-1]['dosen_list'].append(dosen)
                    beban_mengajar[-1]['dosen'] = ", ".join(beban_mengajar[-1]['dosen_list'])

    return {
        'slot_waktu': slot_waktu,
        'ruangan': ruangan,
        'dosen': dosen_libur,
        'beban_mengajar': beban_mengajar,
        'info_sistem': {
            'durasi_sks': durasi_sks,
            'total_slot_per_minggu': len(slot_waktu)
        }
    }

if __name__ == "__main__":
    data = muat_data_excel('data_jadwal.xlsx')
    if data:
        print("Data berhasil dimuat!")
        print(f"Total beban kelas yang akan dijadwalkan (Non-MBKM): {len(data['beban_mengajar'])}")