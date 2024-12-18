<script>
    import { preferences } from '../stores/preferences';

    let navbars   = [];
    let site_logo = '';

    $: site_logo  = $preferences[0]?.site_logo;
    $: navbars    = $preferences[0]?.navbars || [];
</script>


<div class="container">
    <a class="navbar-brand d-flex align-items-center" href="/">
        <img src={site_logo} alt="Brand Logo" class="me-2" style="height: 50px;" />
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
            <li class="nav-item">
                <a class="nav-link" href="/auth/signin"><i class='fa fa-user'></i> Masuk</a>
            </li>
        </ul>
  </div>
</div>