import { writable } from 'svelte/store';

// Inisialisasi store untuk preferences
export const preferences = writable({
    site_title: 'Site Name',
    slideshows: [],
})
