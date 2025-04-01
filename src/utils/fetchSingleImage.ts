interface SingleImageProps {
    id?: string;
    [key: string]: any;
    adeuid?: string; // This allows for any number of additional properties
}
// Original interface
interface SingleImageData {
    id: string;
    src_large: string;
    src_medium: string;
    src_small: string;
    title: string;
    uid: string;
}

// New interface for the Astro component with camelCase properties
interface AstroImageProps {
    id: string;
    srcLarge: string;
    srcMedium: string;
    srcSmall: string;
    altText: string;
    adeuid?: string;
}

import { limitedFetch } from './limitedFetch';

// Function to transform and map data
export async function fetchSingleImage(id: string) {
    const url = `http://127.0.0.1:8011/api/photos/${id}/`;

    try {
        const response = await limitedFetch(url);
        const photo = (await response.json()) as SingleImageData;
        // console.log('FOUND PHOTO');
        // console.log(photo.id);
        // Map to new structure with camelCase properties
        const astroStylePhoto: AstroImageProps = {
            id: photo.id,
            srcLarge: photo.src_large,
            srcMedium: photo.src_medium,
            srcSmall: photo.src_small,
            altText: photo.title, // Here, ensure title is always a string
        };
        //    console.log('FOUND astroStylePhoto');
        //console.log(astroStylePhoto);
        return astroStylePhoto;
    } catch (error) {
        console.error('Error fetching slider image:', error);
    }
}
