// src/utils/loadBlog.ts

// utils/loadBlog.ts
export async function loadBlog(postCount: number = 5) {
    const apiUrl = `https://blog.onelifejapan.com/wp-json/wp/v2/posts?per_page=${postCount}&page=1`;
    //console.log('apiUrl', apiUrl);
    const response = await fetch(apiUrl);

    if (!response.ok) {
        throw new Error(`Failed to fetch posts: ${response.statusText}`);
    }

    const posts = await response.json();

    // Optionally format the posts for your component
    return posts.map((post: any) => ({
        id: post.id,
        title: post.title.rendered,
        slug: post.slug,
        content: post.content.rendered,
        date_published: post.date,
    }));
}


import { limitedFetch } from './limitedFetch';
// export async function loadBlog() {
//     try {
//         const response = await limitedFetch(`http://localhost:8011/api/blog-posts/`); // Update the URL as necessary
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return await response.json();
//     } catch (error) {
//         console.error('Error loading blog posts:', error);
//         return null; // or handle the error as you prefer
//     }
// }

export async function loadPostsInMonth(year: number, month: number) {
    const after = `${year}-${month.toString().padStart(2, '0')}-01T00:00:00`;
    const before = `${year}-${(month + 1).toString().padStart(2, '0')}-01T00:00:00`;

    const response = await fetch(
        `https://blog.onelifejapan.com/wp-json/wp/v2/posts?after=${after}&before=${before}&per_page=100`
    );

    if (!response.ok) {
        throw new Error(`Failed to load posts for ${year}-${month}: ${response.statusText}`);
    }

    return await response.json();
}


// export async function loadPostsInMonth(month: number) {
//     const response = await limitedFetch(`http://127.0.0.1:8011/api/blog-posts/month-count/${month}/`);
//     if (!response.ok) {
//         throw new Error(`Failed to load posts for month ${month}: ${response.statusText}`);
//     }
//     return await response.json();
// }

export async function loadPostsGroupedByYearMonth() {
    const response = await fetch(`https://blog.onelifejapan.com/wp-json/wp/v2/posts?per_page=100`);

    if (!response.ok) {
        throw new Error(`Failed to load grouped posts: ${response.statusText}`);
    }

    const posts = await response.json();

    // Group posts by year and month
    const grouped = posts.reduce((acc: Record<string, any>, post: any) => {
        const date = new Date(post.date);
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');

        const key = `${year}-${month}`;
        if (!acc[key]) {
            acc[key] = [];
        }
        acc[key].push(post);

        return acc;
    }, {});

    return grouped;
}

// export async function loadPostsGroupedByYearMonth() {
//     const response = await limitedFetch(`http://127.0.0.1:8011/api/blog-posts/grouped/`);
//     if (!response.ok) {
//         throw new Error(`Failed to load grouped posts: ${response.statusText}`);
//     }
//     return await response.json();
// }
export async function loadRecentPosts(limit = 10) {
    const response = await fetch(`https://blog.onelifejapan.com/wp-json/wp/v2/posts?per_page=${limit}&order=desc`);

    if (!response.ok) {
        throw new Error(`Failed to fetch recent posts: ${response.statusText}`);
    }

    const posts = await response.json();

    // Format the posts to return only necessary fields
    return posts.map((post: any) => ({
        id: post.id,
        slug: post.slug,
        title: post.title.rendered,
    }));
}



// export async function loadRecentPosts() {
//     const response = await limitedFetch(`http://127.0.0.1:8011/api/blog-posts/recent/`);
//     if (!response.ok) {
//         throw new Error(`Failed to load recent posts: ${response.statusText}`);
//     }
//     return await response.json();
// }

export async function loadPostsGroupedByMonth() {
    const response = await fetch(`https://blog.onelifejapan.com/wp-json/wp/v2/posts?per_page=100`);

    if (!response.ok) {
        throw new Error(`Failed to load posts: ${response.statusText}`);
    }

    const posts = await response.json();

    // Group posts by month name
    const monthCounts = posts.reduce((acc: Record<string, number>, post: any) => {
        const date = new Date(post.date);
        const month = date.toLocaleString('default', { month: 'long' }); // Get full month name

        acc[month] = (acc[month] || 0) + 1;
        return acc;
    }, {});

    return monthCounts;
}


// export async function loadPostsGroupedByMonth() {
//     const response = await limitedFetch(`http://127.0.0.1:8011/api/blog-posts/month-counts/`);
//     if (!response.ok) {
//         throw new Error(`Failed to load month counts: ${response.statusText}`);
//     }
//     return await response.json();
// }

export async function loadPostsByMonth(month: string) {
    const response = await fetch(`https://blog.onelifejapan.com/wp-json/custom/v1/posts-by-month/${month}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch posts for month ${month}: ${response.statusText}`);
    }
    return await response.json();
}
