import { writable } from 'svelte/store';

// Inisialisasi store untuk preferences
export const preference = writable({
    site_title: 'Site Name',
    site_logo: '',
    contact_email: '',
    contact_phone: '',
    navbars: [
        {link: null, icon: null, title: null}
    ],
    slideshows: [
        { image: 'placeholder1.jpg', title: 'Default Slide 1'},
    ],
    social_medias: {
        facebook_url: 'https://www.facebook.com',
        twitter_url: 'https://www.twitter.com',
        instagram_url: 'https://www.instagram.com',
        linkedin_url: 'https://www.linkedin.com',
        youtube_url: 'https://www.youtube.com'
    }
})

