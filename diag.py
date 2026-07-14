from data_parser import muat_data_excel
data = muat_data_excel('data_jadwal.xlsx')
sem6 = [b for b in data['beban_mengajar'] if b['semester'] == 6]
dosen_counts = {}
for b in sem6:
    for d in b['dosen_list']:
        dosen_counts[d] = dosen_counts.get(d, 0) + b['sks']
print('Total SKS Dosen Semester 6:')
for d, sks in sorted(dosen_counts.items(), key=lambda x: x[1], reverse=True):
    print(f'- {d}: {sks} SKS (Libur: {data["dosen"].get(d, [])})')

kelas_counts = {}
for b in sem6:
    k = b['kelas']
    kelas_counts[k] = kelas_counts.get(k, 0) + b['sks']
print('\nTotal SKS per Kelas Semester 6:')
for k, sks in kelas_counts.items():
    print(f'- {k}: {sks} SKS')
    
print(f"\nInfo Sistem: {data['info_sistem']}")
