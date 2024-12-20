<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { apiRequest } from '$lib/api';
    import { htmlToText } from "html-to-text";
    import { DateTime } from 'luxon';
  
    let post = $state({});
    let slug = $page.params.slug + '/';
    let post_excerpt = $state('');
    let publication_date = $state({});
 
    onMount(async () => {
        const response = await apiRequest(`posts/${slug}`);
            post = await response;

        post_excerpt = htmlToText(post.content);

        if (post_excerpt.length > 205) {
            post_excerpt = post_excerpt.substring(0, 205) + '...';
        }

        publication_date = DateTime.fromISO(post.publication_date).toFormat('yyyy-MM-dd');
    });
</script>


<div class="mb-3 post-thumbnail" style="background: url({post.featured_image}) center center no-repeat; background-size: cover;">
    <div class="overlay"></div>
    <div class="container px-3">
        <div class="position-absolute post-thumbnail-label">
            <h1 class="h4 bg-primary post-title fw-bold text-warning mb-0 p-3">{post.title}</h1>
            {#if post.subtitle}
                <p class="post-subtitle bg-warning post-subtitle p-3 m-0">{post_excerpt}</p>
            {/if}
        </div>
    </div>
</div>


<div class="container">
    <div class="row">
        <div class="col-md-3">
            <div class="border shadow-sm">
                <div class="text-center">
                    <h5 class='text-center mb-3 p-3 border-bottom'>Tentang Penulis</h5>
                    <img src={post.author?.profile_picture_url || 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ68D1zB62HiAWZAkQpessCgGpmfvJQUX8Rhg&s'} alt={post.author?.username} class="rounded-circle" width="100" height="100" />
                    <h5>{post.author?.username}</h5>
                </div>
                <div class="p-3">
                    <div class="fa fa-calendar-alt"></div> {publication_date}
                </div>
            </div>
        </div>

        <div class="col-md-9">            
            <article>{@html post.content}</article>
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
        background: rgba(0, 0, 0, 0.1); 
        border-radius: 0.25rem;
    }

    .post-thumbnail {
        position: relative;
        height: 85vh;
    }

    .post-thumbnail-label {
        width: 700px;
        bottom: 15%;        
    }

    .post-title, .post-subtitle {
        opacity: 0.95;
    }
</style>