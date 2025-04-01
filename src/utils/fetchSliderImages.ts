interface SliderImageProps {
    id?: string;
    [key: string]: any; // This allows for any number of additional properties
}

interface SliderImageData {
    id: string;
    tags: string[];
    name: string;
    compiled_image: string;
    order: number;
    uid: string; // Ensure this is included since your JSON structure has it
}

import { limitedFetch } from './limitedFetch';
// Function to load slider images in batch

export async function fetchSliderImage(id: string) {
    const sliderImagesData: SliderImageData[] = [];

    const url = `http://127.0.0.1:8011/api/slider_image/${id}/`;

    try {
        const response = await limitedFetch(url);
        if (!response.ok) {
            console.error(`Error loading slider image with ID: ${id}`);
        }
        const sliderImage: SliderImageData = await response.json();
        return sliderImage;
    } catch (error) {
        console.error('Error fetching slider image:', error);
    }
}

export async function fetchSliderImages(embededSliderImageArray: SliderImageProps[]): Promise<SliderImageData[]> {
    const sliderImagesData: SliderImageData[] = [];

    for (const embededSliderImage of embededSliderImageArray) {
        const url = `http://127.0.0.1:8011/api/slider_image/${embededSliderImage.id}/`;
        try {
            const response = await limitedFetch(url);
            if (!response.ok) {
                console.error(`Error loading slider image with ID: ${embededSliderImage.id}`);
                continue; // Skip this iteration if fetch failed
            }
            const sliderImage: SliderImageData = await response.json();
            // Merge base properties from embededSliderImage with fetched data
            const mergedData = {
                ...sliderImage, // Fetched data
                ...embededSliderImage, // Base properties, including uid
            };
            sliderImagesData.push(mergedData);
        } catch (error) {
            console.error('Error fetching slider image:', error);
        }
    }

    return sliderImagesData;
}
