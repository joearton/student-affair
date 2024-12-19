<script lang="ts">
    import { preference } from '$lib/stores/preference';
    $: site_logo  = $preference.site_logo;
    $: navbars    = $preference.navbars || [];

</script>


<div class="container">
    <a class="navbar-brand d-flex align-items-center" href="/">
        <img src={site_logo} alt="Brand Logo" class="me-2" style="height: 45px;" />
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
            {#each navbars as navbar}
                <li class='nav-item'>
                    <a class='nav-link' href={navbar.link}>
                        <i class={`fa ${navbar.icon}`}></i> {navbar.title}
                    </a>
                </li>
            {/each}
        </ul>
  </div>
</div>