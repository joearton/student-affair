<script lang="ts">
    import { preference } from '$lib/stores/preference';
    
    import Topbar from '$lib/components/Topbar.svelte';
    import Navbar from '$lib/components/Navbar.svelte';
    import Footer from '$lib/components/Footer.svelte';

    let { children } = $props();
    let site_title = $preference.site_title;


</script>


<svelte:head>
    <title>Welcome | {site_title}</title>
</svelte:head>


<div class="topbar bg-primary py-2">
    <Topbar></Topbar>
</div>

<nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-primary">
    <Navbar></Navbar>
</nav>

<main>
    {@render children()}
</main>

<footer class="footer bg-primary text-white py-4">
    <Footer></Footer>
</footer>