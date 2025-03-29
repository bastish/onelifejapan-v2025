// src/utils/loadItineraries.ts
import fs from 'fs/promises';
import path from 'path';

import { limitedFetch } from './limitedFetch';

export async function loadItineraries(slugs: any) {
    const baseUrl = `http://localhost:8011/api/itinerary/`;

    // Check if slugs is an array
    if (Array.isArray(slugs)) {
        const fetchPromises = slugs.map((slug) => {
            // Ensure each slug ends with a slash
            const formattedSlug = slug.toString().endsWith('/') ? slug : `${slug}/`;
            const url = new URL(formattedSlug, baseUrl);
            return limitedFetch(url.toString()).then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            });
        });
        try {
            const results = await Promise.all(fetchPromises);
            // Flatten the results if each API call returns an array of itineraries
            const combinedResults = results.flat();
            return combinedResults; // returns one combined array
        } catch (error) {
            console.error('Error loading itineraries:', error);
            return null;
        }
    } else {
        // Process a single slug as before
        const formattedSlug = slugs.toString().endsWith('/') ? slugs : `${slugs}/`;
        const url = new URL(formattedSlug, baseUrl);
        try {
            const response = await limitedFetch(url.toString());
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return await response.json();
        } catch (error) {
            console.error('Error loading itinerary:', error);
            return null;
        }
    }
}
