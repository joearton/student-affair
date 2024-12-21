<script lang='ts'>
    import { scholarships, filteredScholarships, searchKeyword, ongoingScholarships, getStatusColor, normalizeStatus,formatDescription, formatFaculties, updateFilter, filters } from '$lib/scholarship';
    import { preference } from '$lib/stores/preference';
    import { writable, derived } from "svelte/store";
    import { apiRequest } from '$lib/api';
    import { onMount } from 'svelte'; 

    onMount(async () => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href =
            'https://cdn.jsdelivr.net/npm/@mdi/font/css/materialdesignicons.min.css';
        document.head.appendChild(link);
        try {
            const data = await apiRequest('/scholarship/');
            scholarships.set(data);
        } catch (error) {
            console.error('Error fetching scholarships:', error);
        }        
    });
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
</div>

<div class=''>
    {#if $ongoingScholarships.length === 0}
        <p class="no-scholarship">Tidak ada beasiswa yang tersedia untuk pencarian ini.</p>
    {:else}
        <div class="on-going">
            {#each $ongoingScholarships as scholarship}
                <div class="cards-on-going">
                    <img
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXXW2CIqMG1oFEn-mEZgTcHB9toYSdlZuP3Q&s"
                        alt="Gambar Beasiswa"
                        class="card-image"
                    />
                    <!-- svelte-ignore a11y_consider_explicit_label -->
                    <a href={`/scholarship/${scholarship.id}`} class="icon-link">
                        <i class="fa-solid fa-arrow-right"></i>
                    </a>                                    
                    <div class="status-on-going" style="background-color: {getStatusColor(scholarship.status)};">
                        {normalizeStatus(scholarship.status)}
                    </div>
                    <h3 class="scholarship-name">{scholarship.name}</h3>                               
                    <p class="description">
                        {formatDescription(scholarship.description)}
                    </p>

                    <!-- Details-->
                    <div class="details-on-going">
                        <span>
                            <strong>Sumber:</strong>
                            {normalizeStatus(scholarship.source)}
                        </span>
                        <span>
                            <strong>Tujuan:</strong>
                            {normalizeStatus(scholarship.destination)}
                        </span>
                        <span>
                            <strong>Target:</strong>
                            {normalizeStatus(scholarship.target_audience)}
                        </span>
                        <span>
                            <strong>Kuota:</strong>
                            {scholarship.quota}
                        </span>
                    </div>                                                
                </div>
            {/each}
        </div>
    {/if}
</div>

    
<div class="scholarship-container">
    <div class="scholarship-header">
        <h2 class="title">Daftar Beasiswa Tersedia</h2>
        <span class="fe-separator"></span>
    </div>

    <!-- Search Section -->
    <div class="search-container">
        <div class="col col-12 px-0">
            <div class="d-flex mb-3 fe-shadow">
                <input 
                    type="text" 
                    placeholder="Keyword beasiswa" 
                    class="bg-white py-2 px-3 border-light-gray w-100 fs-subtitle-2 fw-600"
                    bind:value={$searchKeyword}>
                <!-- svelte-ignore a11y_consider_explicit_label -->
                <button class="search-button btn btn-secondary text-primary fs-11 p-3 rounded-0 d-inline-flex align-items-center justify-content-center">
                    <i class="mdi mdi-magnify"></i>
                </button>   
            </div>
        </div>
    </div>

    <!-- Filters Section -->
    <div class="col col-12 px-0">
        <div class="card filter-card mb-4 fe-shadow border-0">
            <div class="card-body">
                <div class="row mx-0 align-items-center">
                    <div class="col col-10 px-0">
                        <div class="fs-subtitle-1 fw-600 mb-0">Filters</div>
                        <div class="yellow-box"></div>
                    </div>
                </div>                         
    
                <!-- Filters Options -->
                <div class="mt-3">
                    <div class="row mx-0">
                        <!-- Filter: Status -->
                        <div class="col col-6 col-md-3 px-0 pb-4">
                            <div class="fs-content-1 fw-600">Status</div>
                            <div class="w-100 mt-2">
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="status-ongoing" on:change={() => updateFilter('status', 'on-going')}>
                                    <label class="custom-control-label" for="status-ongoing">On-Going</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="status-comingsoon" on:change={() => updateFilter('status', 'coming-soon')}>
                                    <label class="custom-control-label" for="status-comingsoon">Coming-Soon</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="status-closed" on:change={() => updateFilter('status', 'closed')}>
                                    <label class="custom-control-label" for="status-closed">Closed</label>
                                </div>
                            </div>
                        </div>
                            
                        <!-- Filter: Tujuan -->
                        <div class="col col-6 col-md-3 px-0 pb-4">
                            <div class="fs-content-1 fw-600">Tujuan</div>
                            <div class="w-100 mt-2">
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="tujuan-umko" on:change={() => updateFilter('tujuan', 'internal')}>
                                    <label class="custom-control-label" for="tujuan-umko">UMKO</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="tujuan-luarumko" on:change={() => updateFilter('tujuan', 'external')}>
                                    <label class="custom-control-label" for="tujuan-luarumko">Universitas di luar UMKO</label>
                                </div>
                            </div>
                        </div>
    
                        <!-- Filter: Sumber -->
                        <div class="col col-6 col-md-3 px-0 pb-4">
                            <div class="fs-content-1 fw-600">Sumber</div>
                            <div class="w-100 mt-2">
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="sumber-internal" on:change={() => updateFilter('sumber', 'internal')}>
                                    <label class="custom-control-label" for="sumber-internal">Beasiswa Internal</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="sumber-eksternal" on:change={() => updateFilter('sumber', 'external')}>
                                    <label class="custom-control-label" for="sumber-eksternal">Beasiswa Eksternal</label>
                                </div>
                            </div>
                        </div>
                                                
                        <!-- Filter: Unit -->
                        <div class="col col-6 col-md-3 px-0 pb-4">
                            <div class="fs-content-1 fw-600">Unit</div>
                            <div class="w-100 mt-2">
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="unit-keguruan-dan-ilmu-pendidikan" on:change={() => updateFilter('unit_names', 'Keguruan dan Ilmu Pendidikan')}>
                                    <label class="custom-control-label" for="unit-keguruan-dan-ilmu-pendidikan">Keguruan dan Ilmu Pendidikan</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="unit-teknik-dan-ilmu-komputer" on:change={() => updateFilter('unit_names', 'Teknik dan Ilmu Komputer')}>
                                    <label class="custom-control-label" for="unit-teknik-dan-ilmu-komputer">Teknik dan Ilmu Komputer</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="unit-pertanian-dan-peternakan" on:change={() => updateFilter('unit_names', 'Pertanian dan Peternakan')}>
                                    <label class="custom-control-label" for="unit-pertanian-dan-peternakan">Pertanian dan Peternakan</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="unit-hukum-dan-ilmu-sosial" on:change={() => updateFilter('unit_names', 'Hukum dan Ilmu Sosial')}>
                                    <label class="custom-control-label" for="unit-hukum-dan-ilmu-sosial">Hukum dan Ilmu Sosial</label>
                                </div>
                            </div>
                        </div>
    
                        <!-- Filter: Target -->
                        <div class="col col-6 col-md-3 px-0 pb-4">
                            <div class="fs-content-1 fw-600">Target</div>
                            <div class="w-100 mt-2">
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="target-mahasiswa-baru" on:change={() => updateFilter('target', 'new-student')}>
                                    <label class="custom-control-label" for="target-mahasiswa-baru">Mahasiswa Baru</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="target-mahasiswa-aktif" on:change={() => updateFilter('target', 'active-student')}>
                                    <label class="custom-control-label" for="target-mahasiswa-aktif">Mahasiswa Aktif</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="target-mahasiswa-lulus" on:change={() => updateFilter('target', 'graduated-student')}>
                                    <label class="custom-control-label" for="target-mahasiswa-lulus">Mahasiswa Lulus</label>
                                </div>
                            </div>
                        </div>

                        <!-- Filter: Kuota -->
                        <div class="col col-6 col-md-3 px-0 pb-4">
                            <div class="fs-content-1 fw-600">Quota</div>
                            <div class="w-100 mt-2">
                                <div class="custom-control custom-checkbox">
                                    <input
                                        type="checkbox"
                                        class="custom-control-input"
                                        id="quota-below-50"
                                        on:change={() => updateFilter('quota', 'below-50')}
                                    />
                                    <label class="custom-control-label" for="quota-below-50">Dibawah 50</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input
                                        type="checkbox"
                                        class="custom-control-input"
                                        id="quota-50-100"
                                        on:change={() => updateFilter('quota', '50-100')}
                                    />
                                    <label class="custom-control-label" for="quota-50-100">50-100</label>
                                </div>
                                <div class="custom-control custom-checkbox">
                                    <input
                                        type="checkbox"
                                        class="custom-control-input"
                                        id="quota-above-100"
                                        on:change={() => updateFilter('quota', 'above-100')}
                                    />
                                    <label class="custom-control-label" for="quota-above-100">Di atas 100</label>
                                </div>
                            </div>
                        </div>

                    </div>
    
                    <!-- Show All Buttons -->
                    <div class="mt-4 d-flex justify-content-end align-items-center">
                        <button
                            type="button"
                            class="fs-content-1 fw-500 text-primary mr-3 cursor-pointer btn-clear"
                            on:click={() => filters.set({ status: [], unit_names: [], sumber: [], tujuan: [], target: [], quota: [] })}
                        >
                        Show All
                        </button>
                    </div>

                </div>
            </div>
        </div>
    </div>
    
    {#if $filteredScholarships.length === 0}
        <p class="no-scholarship">Tidak ada beasiswa yang tersedia untuk pencarian ini.</p>
    {:else}
        <div class="cards-container">
            {#each $filteredScholarships.sort((a, b) => a.name.localeCompare(b.name)) as scholarship}
                <div class="card">
                    <!-- svelte-ignore a11y_consider_explicit_label -->
                    <a href={`/scholarship/${scholarship.id}`} class="icon-link">
                        <i class="fa-solid fa-arrow-right"></i>
                    </a>                                    
                    <h3 class="scholarship-name">{scholarship.name}</h3>
                    <div class="dates">
                        <span><strong>Dibuka:</strong> {new Date(scholarship.start_date).toLocaleString('id-ID', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }).replace(',', ', pukul') || 'TBA'}</span>
                        <span class="separator">|</span>
                        <span><strong>Ditutup: </strong> {new Date(scholarship.end_date).toLocaleString('id-ID', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }).replace(',', ', pukul') || 'TBA'}</span>
                    </div>                                   
                    <div class="status" style="background-color: {getStatusColor(scholarship.status)};">
                        {normalizeStatus(scholarship.status)}
                    </div>
                    <p class="description">
                        {formatDescription(scholarship.description)}
                    </p>

                    <!-- Details-->
                    <div class="details">
                        <span>
                            <strong>Sumber:</strong>
                            {normalizeStatus(scholarship.source)}
                        </span>
                        <span>
                            <strong>Tujuan:</strong>
                            {normalizeStatus(scholarship.destination)}
                        </span>
                        <span>
                            <strong>Target:</strong>
                            {normalizeStatus(scholarship.target_audience)}
                        </span>
                        <span>
                            <strong>Kuota:</strong>
                            {scholarship.quota}
                        </span>
                    </div>

                    <p class="fakultas">
                        <strong>Fakultas:</strong>
                        {formatFaculties(scholarship.unit_names)}
                    </p>                                                 
                </div>

            {/each}
        </div>
        
    {/if}
</div>

<style>
    .scholarship-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 30px 20px 20px;
        display: flex; 
        flex-direction: column; 
        justify-content: center;
        align-items: center;
    }

    .scholarship-header{
        display: row;
        align-items: center;
        margin-bottom: 20px;
    }

    .title {
        font-size: 2rem;
        text-align: center;
        color: #002e5c;
        margin-bottom: 0px;
    }

    .no-scholarship {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
    }

    .card {
        background: #f0f0f0;
        border-radius: 2px;
        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
        padding: 20px;
        width: 100%;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        transition: transform 0.3s, border 0.3s; 
        position: relative; 
        overflow: hidden; 
        margin: 5px; 
        border-radius: 5px;
        border: 2px solid transparent; 
    }

    .card:hover {
        transform: translateY(-5px);
        border-color: #000; 
    }

    .search-container {
        display: flex; 
        flex-wrap: wrap; 
        justify-content: center; 
        padding: 20px;
        width: 100%;
        gap: 20px;
        align-items: center;
    }

    .custom-control-label {
        font-size: 0.9rem;
        font-weight: 400;
        color: #555;
    }

    .search-button {
        background-color: #ffc107; 
        padding: 10px 15px; 
        border-radius: 0; 
        color: #000; 
        min-width: 70px; 
        display: flex; 
        align-items: center;
        justify-content: center; 
    }

    .search-button i {
        font-size: 1.5rem;
    }

    .card.filter-card {
        background-color: #fff !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        border: none;
        padding: 20px;
        margin: 0 auto;
        width: 100%;
        max-width: 1010px;
        text-align: left;
    }

    .on-going {
        display: flex;
        flex-wrap: nowrap; 
        gap: 20px; 
        justify-content: flex-start; 
        padding: 0 10px;
        width: 100%;
        max-width: 1200px; 
        margin: 20px auto; 
        overflow-x: auto; 
        flex: none;
    }

    .card-image {
        width: 100%;
        height: auto;
        object-fit: cover;
        background-color: transparent;
    }
    
    .cards-on-going {
        background: #ffff;
        border-radius: 2px;
        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
        padding: 20px;
        width: 100%;
        max-width: 350px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        transition: transform 0.3s, border 0.3s; 
        position: relative; 
        overflow: hidden; 
        margin: 5px; 
        border-radius: 5px;
        border: 2px solid transparent; 
    }

    .cards-on-going:hover {
        transform: translateY(-5px);
        border-color: #000; 
    }

    .cards-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
        padding: 0 10px;
        width: 100%; 
        max-width: 1200px; 
        margin: 0 auto; 
        flex: none;
    }

    .status-on-going {
        display: inline-block;
        color: #fff;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 0.9rem;
        margin-top: -25px;
        margin-left: -15px;
        width: fit-content;
    }

    .scholarship-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        text-align: left;
    }

    .dates {
        display: flex;
        gap: 5px;
        font-size: 0.9rem;
        color: #555;
        justify-content: flex-start;
        align-items: center;
    }

    .separator {
        font-weight: bold;
        color: #333;
    }

    .status {
        display: inline-block;
        color: #fff;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 0.9rem;
        margin-bottom: -2px;
        width: fit-content;
    }

    .description {
        font-size: 1rem;
        color: #444;
        white-space: pre-wrap;
        line-height: 1.5;
    }

    .fakultas {
        font-size: 0.9rem;
        color: #555;
        justify-content: flex-start;
        white-space: pre-wrap;
        line-height: 1.5;
    }

    .details {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
        font-size: 0.9rem;
        color: #555;
    }

    .details span {
        flex: 1;
        text-align: left;
        padding: 2px; 
        display: flex;
        flex-direction: column; 
    }
    
    .details-on-going {
        display: grid;
        grid-template-columns: repeat(2, 1fr); 
        grid-auto-rows: auto; 
        gap: 10px; 
        padding: 10px;
    }

    .details-on-going span {
        flex: 1;
        text-align: left;
        padding: 2px; 
        display: flex;
        flex-direction: column; 
    }

    .yellow-box {
        background-color: #f5c13a; 
        width: 3rem; 
        height: 0.2rem; 
        margin-top: 0rem; 
    }

    .separator {
        margin: 0 3px; 
    } 
        
    .fe-shadow {
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .fe-separator {
        display: block;
        background-color: #f5c13a;
        width: 3rem;
        height: 0.4rem;
        margin: 0.5rem 0;
    }

    .fe-separator {
            display: block;
            background-color: #f5c13a;
            width: 3rem;
            height: 0.4rem;
            margin: 0.2rem auto; 
    }

    .mt-4.d-flex {
        gap: 20px;
    }

    .fs-content-1 {
        margin-right: 0; 
    }

    .icon-link {
        position: absolute;
        top: 0;
        right: 0;
        background-color: #f5c13a;
        color: #000;
        width: 3rem; 
        height: 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        font-size: 1.2rem; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease, transform 0.3s ease;
        border-radius: 0; 
    }

    .icon-link i {
        transform: rotate(-45deg); 
        transition: transform 0.3s ease; 
    }

    .icon-link:hover {
        background-color: #ffc107; 
        transform: scale(1.1); 
    }

    .btn-clear {
        background: none; 
        border: none; 
        padding: 0; 
        color: inherit; 
        cursor: pointer; 
        font: inherit; 
        text-decoration: none; 
    }

    @media (max-width: 576px) and (max-height: 775px) {
        .separator {
            display: none;
        }
    }

    @media (max-width: 768px){
        .on-going {
            flex-direction: column; 
            gap: 10px; 
            padding: 0;
            align-items: center; 
        }
        .separator {
            display: none;
        }
    }


    @media (min-width: 768px) {
        .card {
            width: calc(100% - 40px);
        }
        .search-container {
            width: calc(100% - 40px);
        }
        .cards-container {
            padding: 0 5px; 
            gap: 10px; 
        }
        
    }

    @media (min-width: 1200px) {
        .card {
            max-width: 1000px;
        }
        .search-container {
            width: calc(100% - 40px);
        }
    }

    @media (max-width: 768px) {
        .dates {
            gap: 3px; 
        }
        .search-container {
            max-width: 100%;
        }
        .cards-on-going img {
            display: none;
        }
        .status-on-going {
            margin-top: 0px;
            margin-left: 0px;
        }
        .cards-on-going{
            width: 100%;
            max-width: 500px;
        }
    }
</style>