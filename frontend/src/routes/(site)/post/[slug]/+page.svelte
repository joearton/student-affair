<script lang="ts">
    import { onMount } from "svelte";
    import { getPost } from "$lib/blog";
    import { page } from "$app/state";
    import SidePostMenu from "$lib/components/SidePostMenu.svelte";

    let slug = page.params.slug;
    let post = $state({
        featured_image: "",
        title: "",
        status: "",
        slug: "",
        subtitle: "",
        post_excerpt: "",
        author: {
            profile_picture_url: "",
            username: "",
        },
        publication_date: "",
        content: "",
    });

    onMount(async () => {
        post = await getPost({ slug: slug });
    });
</script>

<svelte:head>
    <title>{post.title}</title>
</svelte:head>

<!-- Thumbnail -->
<div
    class="mb-3 post-thumbnail"
    style="background: url({post.featured_image}) bottom center no-repeat; background-size: cover;"
>
    <div class="overlay"></div>
    <div class="container px-3">
        <div class="position-absolute post-thumbnail-label">
            <h1 class="h4 bg-primary post-title fw-bold text-warning mb-0 p-3">
                {post.title}
            </h1>
            {#if post.subtitle}
                <p class="post-subtitle bg-warning post-subtitle p-3 m-0">
                    {post.post_excerpt}
                </p>
            {/if}
        </div>
    </div>
</div>

<!-- Profil Penulis -->
<div class="container mt-5">

    <div class="info bg-body-secondary rounded-2 p-4 mb-5">
        <p>Date Publication: {post.publication_date}</p>
        <div class="btn status bg-success rounded-5 py-1 px-3 text-white mb-2">{post.status}</div>
        <div class="other-info d-flex justify-content-between text-start mt-3">
            <div><strong>Level:</strong> <br> Bachelor</div>
            <div><strong>Source:</strong> <br> Internal Scholarship</div>
            <div><strong>Goal:</strong> <br> UMKO</div>
            <div><strong>Awarde:</strong> <br> New Students</div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-3">
            <div class="border shadow-sm rounded-5 mb-4">
                <div class="text-center">
                    <h5 class="text-center mb-3 p-3 border-bottom">
                        Tentang Penulis
                    </h5>
                    <img
                        src={post.author?.profile_picture_url ||
                            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ68D1zB62HiAWZAkQpessCgGpmfvJQUX8Rhg&s"}
                        alt={post.author?.username}
                        class="rounded-circle"
                        width="100"
                        height="100"
                    />
                    <h5>{post.author?.username}</h5>
                </div>
                <div class="p-3">
                    <div class="fa fa-calendar-alt"></div>
                    {post.publication_date}
                </div>
                <div class="sosmed p-2 text-center border-top">
                    <a
                        href="https://www.instagram.com/joe_arton?igsh=MTd6YzZkODY5Z3JndQ=="
                        target="_blank"
                    >
                        <i class="bi bi-instagram"></i>
                    </a>
                    <a href="https://www.facebook.com/" target="_blank">
                        <i class="bi bi-facebook"></i>
                    </a>
                    <a href="https://www.linkedin.com/" target="_blank">
                        <i class="bi bi-linkedin"></i>
                    </a>
                    <a href="https://www.twitter.com/" target="_blank">
                        <i class="bi bi-twitter-x"></i>
                    </a>
                </div>
            </div>
            <div class="other-post p-2">
                <h6>Other Post</h6>

                <SidePostMenu />
            </div>
        </div>

        <!-- Info Content -->
        <div class="col-md-9 shadow-sm mb-4 border-2">

            

            <article>{@html post.content}</article> <!-- Content -->

            <div
                class="apply w-100 shadow-sm bg-primary d-flex justify-content-between p-3 align-items-center mt-4"
            >
                <p class="text-white fw-semibold">Don't miss the chance!</p>
                <button type="submit" class="btn btn-warning rounded-0 fw-bold text-primary"
                    >Apply Now <i class="bi bi-arrow-right-circle-fill"></i>
                </button>
            </div>

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
        box-shadow: 1px 1px 8px rgb(255, 255, 255, 0.2);
    }

    .post-title,
    .post-subtitle {
        opacity: 0.95;
    }

    .sosmed a .bi {
        color: #002e5c;
        margin: 0.5rem;
        transition: all 0.4s ease;
    }

    .sosmed a .bi:hover {
        color: #ffcc00;
    }

    .info:hover {
        transition: all 0.4s ease;
        transform: scale(1.02);
        box-shadow: 0 0 4px 2px rgba(0, 0, 0, 0.25);
    }
</style>
