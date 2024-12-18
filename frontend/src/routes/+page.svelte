<script>
    import { preferences } from '../stores/preferences';

</script>


<div>

  <!-- Caraousel -->
<div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner">
        {#each $preferences?.slideshows as slideshow, index}
            <div class="carousel-item {index === 0 ? 'active' : ''}">
                <img src={slideshow.image} class="d-block w-100" alt={slideshow.title}>
            </div>
        {/each}
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
    </button>
</div>

  
  <!-- Features Section -->
  <div class="features-section bg-white py-5">
    <div class="container text-center">
      <div class="row">
        <div class="col-md-3">
          <h2>#1</h2>
          <p>Universitas terbaik</p>
        </div>
        <div class="col-md-3">
          <h2>100+</h2>
          <p>Program unggulan</p>
        </div>
        <div class="col-md-3">
          <h2>50+</h2>
          <p>Dosen bersertifikasi</p>
        </div>
        <div class="col-md-3">
          <h2>10+</h2>
          <p>Fakultas terbaik</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Mahasiswa Baru -->
  <div class="new-student-section py-5 bg-light">
    <div class="container text-center">
      <h2 class="fw-bold">Pendaftaran Mahasiswa Baru</h2>
      <p class="lead">Bergabunglah bersama kami untuk masa depan lebih cerah.</p>
      <a href="#" class="btn btn-primary">Daftar Sekarang</a>
    </div>
  </div>

  <!-- Life Section -->
  <div class="life-section py-5">
    <div class="container">
      <h2 class="text-center fw-bold">Kehidupan & Akomodasi Kampus</h2>
      <div class="row">
        <div class="col-md-6">
          <img src="image-1.jpg" class="img-fluid rounded" alt="Kehidupan Kampus">
        </div>
        <div class="col-md-6 d-flex align-items-center">
          <p>Kenali lebih jauh berbagai fasilitas yang ada di kampus kami untuk mendukung pengalaman belajar yang
            menyenangkan.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Research Section -->
  <div class="research-section bg-light py-5">
    <div class="container">
      <h2 class="text-center fw-bold">Penelitian Unggulan</h2>
      <p class="text-center">Kami mendukung penelitian terbaik untuk pengembangan ilmu pengetahuan dan teknologi.</p>
      <div class="text-center">
        <a href="#" class="btn btn-primary">Lihat Penelitian</a>
      </div>
    </div>
  </div>

</div>