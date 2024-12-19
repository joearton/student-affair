<script lang='ts'>
    import { preference } from '$lib/stores/preference';
    import { apiRequest } from '$lib/api';
    import { onMount } from 'svelte';

    let posts = $state([{
        title          : '',
        content        : '',
        slug           : '',
        featured_image : ''
    }]);

    onMount(async () => {
        try {
            posts = await apiRequest('/posts/');
        } catch (error) {
        } finally {
        }        
    })

</script>


<div class=''>

    <!-- Caraousel -->
    <div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
            {#each $preference?.slideshows as slideshow, index}
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

    <!-- Mahasiswa Baru -->
    <div class="new-student-section py-5 position-relative">
        <div class="container text-center py-5">
            <h2 class="fw-bold display-5 text-primary mb-1">Pendaftaran Mahasiswa Baru</h2>
            <p class="lead mb-4">Bergabunglah bersama kami untuk masa depan lebih cerah.</p>
            <a href="https://pmb.umko.ac.id" class="btn btn-primary btn-lg px-5 py-2 shadow-lg rounded-pill">
                <i class="fa fa-link"></i> Daftar Sekarang
            </a>
        </div>
    </div>
  
    <!-- Features Section -->
    <div class="features-section py-5 bg-primary">
        <div class="container text-center">
            <h2 class="fw-bold mb-2 text-warning">Mengapa Memilih Kami?</h2>
            <p class="mb-5 text-white">Kami memberikan yang terbaik untuk memastikan kesuksesan Anda.</p>
            <div class="row gy-4">
                <div class="col-md-3">
                    <div class="feature-card py-4 px-3 bg-white shadow rounded">
                        <div class="icon-container mb-3">
                            <i class='fa fa-university'></i>
                        </div>
                        <h3 class="fw-bold">+11</h3>
                        <p>Pilihan Program Studi</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="feature-card py-4 px-3 bg-white shadow rounded">
                        <div class="icon-container mb-3">
                            <i class="fa fa-user-graduate"></i>
                        </div>
                        <h3 class="fw-bold">5000+</h3>
                        <p class="text-muted">Alumni telah Bekerja</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="feature-card py-4 px-3 bg-white shadow rounded">
                        <div class="icon-container mb-3">
                            <i class="fa fa-users"></i>
                        </div>
                        <h3 class="fw-bold">50+</h3>
                        <p class="text-muted">Dosen Tersertifikasi</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="feature-card py-4 px-3 bg-white shadow rounded">
                        <div class="icon-container mb-3">
                            <i class="fa fa-trophy"></i>
                        </div>
                        <h3 class="fw-bold">100+</h3>
                        <p class="text-muted">Prestasi Dosen dan Mahasiswa</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
  
    <div class="post-section py-5">
        <div class="container">
            <h2 class="fw-bold text-center mb-4">Latest Posts</h2>    
            {#if posts.length === 0}
                <p class="text-muted text-center">No posts available at the moment.</p>
            {:else}
                <div class="row row-cols-1 row-cols-md-3 g-4">
                    {#each posts as post}
                        <div class="col">
                            <div class="card h-100 shadow-sm">
                                <img 
                                    src={post.featured_image || 'https://via.placeholder.com/300x200'} 
                                    class="card-img-top" 
                                    alt={post.title || 'Post Image'} 
                                />
                                <div class="card-body">
                                    <h5 class="card-title">{post.title}</h5>
                                    <p class="card-text text-muted">{post.content || 'No description available.'}</p>
                                </div>
                                <div class="card-footer text-end">
                                    <a href={`/posts/${post.slug}`} class="btn btn-primary btn-sm">Read More</a>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    </div>

</div>


<style>
    .new-student-section {
        background: #ffffff;
    }

    .new-student-section a:hover {
        transform: scale(1.25);
        transition: all 0.5s ease-in-out;
    }

    .features-section {
        clip-path: url(#path-3);
    }

    .feature-card:hover {
        transform: translateY(-7px);
        transition: all 0.5s ease-in-out;
    }

    .icon-container {
        display: inline-flex;
        justify-content: center;
        align-items: center;
        width: 90px;
        height: 90px;
        background-color: rgba(0, 123, 255, 0.1); /* Warna background transparan */
        border-radius: 50%;
        margin: 0 auto;
        font-size: 25px;
    }


</style>