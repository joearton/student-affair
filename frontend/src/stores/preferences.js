import { writable } from 'svelte/store';

// Inisialisasi store untuk preferences
export const preferences = writable({
    site_title: 'Site Name',
    slideshows: [
        { image: 'placeholder1.jpg', title: 'Default Slide 1'},
    ],
})
