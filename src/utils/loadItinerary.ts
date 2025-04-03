// src/utils/loadItinerary.ts
import fs from 'fs/promises';
import path from 'path';

import { limitedFetch } from './limitedFetch';
export async function loadItinerary(id: string) {
    try {
        const url = `http://localhost:8011/api/itinerary/${id}/`;
        console.log(url);
        const response = await limitedFetch(url); // Update the URL as necessary
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading itinerary:', error);
        return null;
    }
}
