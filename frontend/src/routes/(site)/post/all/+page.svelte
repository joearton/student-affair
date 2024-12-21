<script lang='ts'>
    import { preference } from '$lib/stores/preference';
    import { apiRequest } from '$lib/api';
    import { onMount } from 'svelte';
    import { htmlToText } from "html-to-text";
    import { DateTime } from 'luxon';

    let maxLength = 100;
    let posts = $state([{
        title          : '',
        content        : '',
        slug           : '',
        featured_image : ''
    }]);

    onMount(async () => {
        try {
            posts = await apiRequest('posts/');
            posts = posts.results;
            posts = posts.map(post => {
                post.publication_date = DateTime.fromISO(post.publication_date).toLocaleString(DateTime.DATE_FULL);
                return post;
            });
        } catch (error) {
        } finally {
        }        
    })

</script>


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
                                    { htmlToText(post.content).slice(0, maxLength) } ...
                                </p>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>
