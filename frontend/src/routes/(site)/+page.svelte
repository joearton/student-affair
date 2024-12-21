<script lang='ts'>
    import { preference } from '$lib/stores/preference';
    import { onMount } from 'svelte';
    import { getPosts } from '$lib/blog';

    let posts = $state([{
        title           : '',
        content          : '',
        slug             : '',
        featured_image   : '',
        publication_date : '',
        post_excerpt     : ''
    }]);

    onMount(async () => {
        try {
            posts = await getPosts();
        } catch (error) {
        } finally {
        }        
    })

</script>


<div class=''>

    <!-- Caraousel -->
    <div id="front-carousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
            {#each $preference?.slideshows as slideshow, index}
                <div class="carousel-item {index === 0 ? 'active' : ''}">
                    <img src={slideshow.image} class="d-block w-100" alt={slideshow.title}>
                </div>
            {/each}
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#front-carousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#front-carousel" data-bs-slide="next">
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
                    {#each posts.slice(0, 6) as post}
                        <div class="col">
                            <div class="card post-item h-100 shadow-lg">
                                <a class="card-title mb-1" href={`/post/${post.slug}`} aria-label="{post.title}">
                                    <div class="post-thumbnail" style="background: url({post.featured_image}) center center no-repeat; background-size: cover;"></div>
                                </a>
                                <div class="card-body px-4">
                                    <div class='py-2 text-sm'>
                                        <i class='fa fa-calendar-alt'></i> {post.publication_date}
                                    </div>
                                    <a class="card-title" href={`/post/${post.slug}`}>
                                        <h5 class='fw-bold'>{post.title}</h5>
                                    </a>
                                    <p class="card-text text-muted py-3">
                                        {post.post_excerpt}
                                    </p>
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
    .text-sm {
        font-size: 13px;
    }

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

    .post-thumbnail {
        position: relative;
        height: 215px;
    }



</style>