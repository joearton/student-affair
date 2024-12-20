<script lang="ts">
    import { onMount } from 'svelte';
    import { getPost } from '$lib/blog';
    import { page } from '$app/state';

    let slug = page.params.slug;
    let post = $state({
        featured_image: '',
        title: '',
        subtitle: '',
        post_excerpt: '',
        author: {
            profile_picture_url: '',
            username: ''
        },
        publication_date: '',
        content: ''
    });
 
    onMount(async () => {
        post = await getPost({slug: slug})
    });
</script>


<div class="mb-3 post-thumbnail" style="background: url({post.featured_image}) bottom center no-repeat; background-size: cover;">
    <div class="overlay"></div>
    <div class="container px-3">
        <div class="position-absolute post-thumbnail-label">
            <h1 class="h4 bg-primary post-title fw-bold text-warning mb-0 p-3">{post.title}</h1>
            {#if post.subtitle}
                <p class="post-subtitle bg-warning post-subtitle p-3 m-0">{post.post_excerpt}</p>
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
                    <div class="fa fa-calendar-alt"></div> {post.publication_date}
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
        height: 75vh;
    }

    .post-thumbnail-label {
        width: 70%;
        bottom: 7%;        
    }

    .post-title, .post-subtitle {
        opacity: 0.95;
    }
</style>