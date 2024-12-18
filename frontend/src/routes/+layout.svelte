<script lang="ts">
    let { children }  = $props();
    let section_title = 'Welcome';

    import '../app.scss';

    if (typeof window !== 'undefined') {
        // @ts-ignore
        import('bootstrap/dist/js/bootstrap.bundle.min.js');
    }    

    import { onMount } from 'svelte';
    import { apiRequest } from '../api';
    import { preferences } from '../stores/preferences';

    import Topbar from '../widgets/Topbar.svelte';
    import Navbar from '../widgets/Navbar.svelte';
    import Footer from '../widgets/Footer.svelte';


    onMount(async () => {
        const data = await apiRequest('/preferences/');
        let site_title = data
        preferences.set(data);
    });

</script>

<svelte:head>
    <title>{section_title}</title>
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

<Footer></Footer>
