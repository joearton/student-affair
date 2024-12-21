import { apiRequest } from '$lib/api';
import { DateTime } from 'luxon';
import { htmlToText } from 'html-to-text';


export async function getPosts({ search = '', category = '', tag = '', slug = '', id = '' } = {}) {
    const params: { 
        search?: string;
        category?: string;
        tag?: string,
        slug?: string,
        id?: string
    } = {};
    
    if (search) params.search = search;
    if (category) params.category = category;
    if (tag) params.tag = tag;
    if (slug) params.slug = slug;
    if (id) params.id = id; 

    // Menyusun endpoint dengan query string
    const queryString = new URLSearchParams(params).toString();
    const endpoint = `posts/?${queryString}`;

    const response = await apiRequest(endpoint, 'GET');
    const posts = response.results;

    // Format setiap post
    return posts.map((post: {content: string, publication_date: string}) => ({
        ...post,
        post_excerpt: createExcerpt(post.content),
        publication_date: formatPublicationDate(post.publication_date),
    }));
}


export async function getPost({ slug = '', id = '' } = {}) {
    if (!slug && !id) {
        throw new Error('Either slug or id must be provided to get a post.');
    }

    // Memanggil fungsi getPosts dengan filter slug atau id
    const posts = await getPosts({ slug, id });

    // Mengembalikan post pertama jika ditemukan, atau null jika tidak ada
    return posts.length > 0 ? posts[0] : null;
}



function createExcerpt(content: string) {
    const text = htmlToText(content);
    return text.length > 205 ? text.substring(0, 205) + '...' : text;
}

function formatPublicationDate(date:string) {
    return DateTime.fromISO(date).toFormat('yyyy-MM-dd');
}
