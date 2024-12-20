<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { apiRequest } from '$lib/api';
  
    let post = $state({});
    let slug = $page.params.slug + '/';
  
    onMount(async () => {
      const response = await apiRequest(`posts/${slug}`);
      post = await response;
    });
</script>


<div class="mb-3 post-thumbnail" style="background: url({post.featured_image}) center center no-repeat; background-size: cover;">
    <div class="overlay"></div>
    <div class="container px-3">
        <div class="position-absolute post-thumbnail-label">
            <h1 class="h4 bg-primary post-title fw-bold text-warning mb-0 p-3">{post.title}</h1>
            {#if post.subtitle}
                <p class="h5 bg-warning post-subtitle p-3 m-0">{post.subtitle}</p>
            {/if}
        </div>
    </div>
</div>

<div class="container">
    <div class="row">
        <div class="col-md-12">
            {post.content}
        </div>
    </div>
</div>
  

<style>
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5); 
        border-radius: 0.25rem;
    }

    .post-thumbnail {
        position: relative;
        height: 90vh;
    }

    .post-thumbnail-label {
        width: 700px;
        bottom: 50%;
    }    
</style>