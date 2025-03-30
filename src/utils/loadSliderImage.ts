// // src/utils/loadItinerary.ts
// import fs from 'fs/promises';
// import path from 'path';

// export async function loadItinerary(id: string) {
//     try {
//         const filePath = path.join(process.cwd(), `data/itinerary_${id}.json`);
//         const jsonData = await fs.readFile(filePath, 'utf8');
//         return JSON.parse(jsonData);
//     } catch (error) {
//         console.error('Error loading itinerary:', error);
//         return null; // or handle the error as you prefer
//     }
// }

// src/utils/loadItinerary.ts
import { limitedFetch } from './limitedFetch';
export async function loadSliderImage(id: string) {
    const url = `http://localhost:8011/api/slider_image/${id}/`;
    // console.log(url);
    try {
        const response = await limitedFetch(url); // Update the URL as necessary
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading itinerary:', error);
        console.error('bad url: ', url);
        return null;
    }
}
