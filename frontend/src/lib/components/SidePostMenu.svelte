<script lang="ts">
    import { preference } from "$lib/stores/preference";
    import { onMount } from "svelte";
    import { getPosts } from "$lib/blog";

    let posts = $state([
        {
            title: "",
            slug: "",
            featured_image: "",
        },
    ]);

    onMount(async () => {
        try {
            posts = await getPosts();
        } catch (error) {
        } finally {
        }
    });
</script>

<div class="side-post-menu w-auto mb-3">
    {#if posts.length === 0}
        <p class="text-muted text-center">No posts available at the moment.</p>
    {:else}
        {#each posts.slice(0, 6) as post}
            <div class="title-thumbnail d-flex mb-3 gap-2">
                <img src={post.featured_image} alt="" class="post-thumbnail" />
                <a href={`/post/${post.slug}`} class="card-title mb-1"
                    >{post.title}</a
                >
            </div>
        {/each}
    {/if}
</div>

<style>
    .side-post-menu {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
    }
    .title-thumbnail .post-thumbnail {
        width: 100px;
        height: 100px;
        object-fit: cover;
    }
    .title-thumbnail .card-title {
        font-size: 0.8rem;
        color: #3a3a3a;
        font-weight: 600;
        transition: all 0.4s ease;
    }
    .title-thumbnail .card-title:hover {
        color: #002e5c;
    }
</style>
