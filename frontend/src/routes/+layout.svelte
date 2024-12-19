<script lang="ts">
    import { onMount } from 'svelte';
    import { apiRequest } from '$lib/api';
    import { preference } from '$lib/stores/preference';
    
    let { children } = $props();
    let is_loading  = $state(true); 

    onMount(async () => {
        try {
            const data = await apiRequest('/preferences/');
            preference.set(data);
        } catch (error) {
        } finally {
            is_loading = false; 
        }
    });

    // import bootstrap
    import '../app.scss';
    if (typeof window !== 'undefined') {
        // @ts-ignore
        import('bootstrap/dist/js/bootstrap.bundle.min.js');
    }    

    import ClipPath from '$lib/components/ClipPath.svelte'

</script>


<main>
    {#if is_loading}
        <div class="d-flex justify-content-center align-items-center" style="height: 100vh;">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    {:else}
        <ClipPath></ClipPath>
        {@render children()}
    {/if}
</main>

