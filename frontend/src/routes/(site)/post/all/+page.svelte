<script lang='ts'>
    import { onMount } from 'svelte';
    import { getPosts } from '$lib/blog';
    import type { Post } from '$lib/types/post';
    import NoDataAvailable from '$lib/components/NoDataAvailable.svelte';

    let searchQuery = $state('');

    let response = { results: [] };
    let posts: Post[] = $state([]);
    let isLoading = $state(true);

    async function updatePost(query: string = '') {
        try {
            response = await getPosts({search: query, page: 1, limit: 9 });
            posts = response.results;
        } catch (error) {
            console.error('Error fetching posts:', error);
        } finally {
            isLoading = false;
        }
    }
    
    onMount(async () => {
        await updatePost();
    })

    function handlePostFilter() {
        updatePost(searchQuery);
    }

</script>


<div class="post-section py-5">
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="post-sidebar shadow-sm py-4 px-4 rounded">                
                    <!-- Search Bar -->
                    <div class="post-search mb-4">
                        <input oninput={handlePostFilter} bind:value={searchQuery} type="text" class="form-control" placeholder="Search posts">
                    </div>
                
                    <!-- Categories Section -->
                    <div class="post-categories mb-4">
                        <h5 class="fw-bold text-secondary mb-3">Categories</h5>
                        <ul class="list-unstyled">
                            <li><a href="#" class="text-decoration-none text-dark d-flex align-items-center">
                                <i class="fa fa-folder me-2 text-primary"></i> Technology</a>
                            </li>
                            <li><a href="#" class="text-decoration-none text-dark d-flex align-items-center">
                                <i class="fa fa-folder me-2 text-primary"></i> Design</a>
                            </li>
                            <li><a href="#" class="text-decoration-none text-dark d-flex align-items-center">
                                <i class="fa fa-folder me-2 text-primary"></i> Development</a>
                            </li>
                        </ul>
                    </div>
                
                    <!-- Tags Section -->
                    <div class="post-tags">
                        <h5 class="fw-bold text-secondary mb-3">Tags</h5>
                        <ul class="list-inline">
                            <li class="list-inline-item"><a href="#" class="badge bg-primary text-white text-decoration-none">HTML</a></li>
                            <li class="list-inline-item"><a href="#" class="badge bg-secondary text-white text-decoration-none">CSS</a></li>
                            <li class="list-inline-item"><a href="#" class="badge bg-warning text-dark text-decoration-none">JavaScript</a></li>
                            <li class="list-inline-item"><a href="#" class="badge bg-info text-dark text-decoration-none">Bootstrap</a></li>
                        </ul>
                    </div>
                </div>
                
            </div>
            <div class="col-md-9">
                {#if posts.length}
                    {#each posts as post, index}
                        <div class="post-item mb-3">
                            {#if isLoading}
                                <div class="shimmer-wrapper">
                                    {#each Array(6) as _}
                                        <div class="shimmer-post mb-3"></div>
                                    {/each}
                                </div>
                            {:else}
                                {#if index === 0}
                                    <div class="post-banner position-relative shadow-sm" style="background: url({post.featured_image}) bottom center no-repeat; background-size: cover;">
                                        <div class="position-absolute bottom-0">
                                            <div class="bg-warning w-75 mx-3 p-3">
                                                <h5 class='fw-bold'><a href={`/post/${post.slug}`}>{post.title}</a></h5>
                                                <div class="post-date text-sm">
                                                    <i class="fa fa-calendar-alt"></i> {post.publication_date}
                                                </div>
                                            </div>
                                            <div class="bg-primary text-white p-3 opacity-75">
                                                <p class="post-excerpt m-0">{ post.post_excerpt }</p>
                                            </div>
                                        </div>
                                    </div>
                                {:else}
                                    <div class="post-list p-3">
                                        <div class="row">
                                            <div class="col-md-3">
                                                <div class="post-thumbnail" style="background: url({post.featured_image}) center center no-repeat; background-size: cover;"></div>
                                            </div>
                                            <div class="col-md-9">                                    
                                                <h5 class='fw-bold'><a href={`/post/${post.slug}`}>{post.title}</a></h5>
                                                <div class="post-date text-sm">
                                                    <i class="fa fa-calendar-alt"></i> {post.publication_date}
                                                </div>                                    
                                                <p class="post-excerpt text-muted py-3">{ post.post_excerpt }</p>
                                            </div>
                                        </div>        
                                    </div>
                                {/if}
                            {/if}
                        </div>
                    {/each}    
                    <nav>
                        <ul class="pagination">
                        </ul>
                    </nav>            
                {:else}
                    <NoDataAvailable searchQuery=''></NoDataAvailable>
                {/if}    
            </div>
        </div>
    </div>
</div>


<style>
    .shimmer-wrapper {
        display: grid;
        gap: 1rem;
    }

    .shimmer-post {
        height: 80px;
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        border-radius: 8px;
        animation: shimmer 1.5s infinite;
    }

    @keyframes shimmer {
        from {
            background-position: 200% 0;
        }
        to {
            background-position: -200% 0;
        }
    }

    .post-sidebar {
        background-color: #eeebeb;
        position: sticky;
    }

    .post-banner {
        height: 425px;
    }

    .post-item {
        background: #eeebeb;
    }

    .post-list {
        .post-excerpt {
            font-size: 15px;
        }
    }

    .post-date {
        font-size: 13px;
    }

    .post-thumbnail {
        position: relative;
        height: 150px;
    } 

</style>