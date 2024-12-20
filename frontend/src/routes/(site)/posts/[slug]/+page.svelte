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
  
  <h1>{post.title}</h1>
  <p>{post.content || 'Please wait...'}</p>
  