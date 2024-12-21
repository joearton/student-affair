# Student Affair Site

**Student Affair Site** adalah sebuah aplikasi berbasis web untuk membantu mengelola administrasi dan kegiatan kemahasiswaan, termasuk pendaftaran, pelaporan, dan manajemen kegiatan.

## Fitur Utama
- **Pendaftaran Kegiatan**: Mahasiswa dapat mendaftar untuk berbagai kegiatan yang diselenggarakan oleh kampus.
- **Pelaporan**: Mahasiswa dapat mengunggah laporan kegiatan yang telah diikuti.
- **Manajemen Kegiatan**: Admin dapat mengelola data kegiatan, mahasiswa peserta, dan laporan.
- **Notifikasi**: Pengguna mendapatkan notifikasi terkait pendaftaran dan status kegiatan.

## Teknologi yang Digunakan
- **Backend**: Django (Python)
- **Frontend**: Svelte
- **Database**: PostgreSQL
- **Otentikasi**: Django-Allauth
- **Celery**: Untuk penjadwalan tugas dan pengiriman email notifikasi

## Instalasi dan Penggunaan

### Prasyarat
Pastikan Anda sudah menginstal:
- Python 3.8 atau lebih baru
- PostgreSQL
- Redis
- Node.js dan npm (untuk mengelola dependensi frontend)

### Langkah Instalasi
1. **Clone repository ini**:
   ```bash
   git clone https://github.com/username/student-affair-site.git
   cd student-affair-site
   ```

2. **Buat dan aktifkan virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk pengguna Windows: venv\Scripts\activate
   ```

3. **Instal dependensi Python**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi database**:
   - Buat database PostgreSQL.
   - Perbarui pengaturan database di `settings.py`.

5. **Jalankan migrasi**:
   ```bash
   python manage.py migrate
   ```

6. **Jalankan server pengembangan backend**:
   ```bash
   python manage.py runserver
   ```
   Akses backend di [http://localhost:8000](http://localhost:8000).

### Konfigurasi Frontend
1. Masuk ke direktori frontend:
   ```bash
   cd frontend
   ```

2. Install dependensi frontend:
   ```bash
   npm install
   ```

3. Jalankan server pengembangan frontend:
   ```bash
   npm run dev
   ```
   Akses frontend di [http://localhost:5173](http://localhost:5173).

### Konfigurasi Celery
1. Jalankan Redis sebagai broker:
   ```bash
   redis-server
   ```

2. Jalankan worker Celery:
   ```bash
   celery -A project_name worker --loglevel=info
   ```

## Penggunaan
1. Login ke aplikasi sebagai admin menggunakan akun yang sudah dibuat sebelumnya.
2. Tambahkan data kegiatan dan mahasiswa peserta.
3. Mahasiswa dapat mulai mendaftar ke kegiatan.
4. Admin dapat memantau pelaporan dan memberikan persetujuan.

## Kontribusi
Kami menyambut kontribusi dari komunitas. Silakan ikuti langkah berikut untuk berkontribusi:
1. Fork repository ini.
2. Buat branch fitur atau perbaikan di lokal Anda.
3. Kirimkan pull request.

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

**Catatan**: Pastikan Anda memperbarui dokumen ini dengan informasi spesifik terkait proyek Anda.
