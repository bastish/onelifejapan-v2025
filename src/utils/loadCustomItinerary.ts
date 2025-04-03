// src/utils/loadCustomItinerary.ts

import { limitedFetch } from './limitedFetch';
export async function loadCustomItinerary(id: string) {
    try {
        //console.log(`http://localhost:8011/api/custom_itinerary/${id}/`);
        const response = await limitedFetch(`http://localhost:8011/api/custom_itinerary/${id}/`); // Update the URL as necessary
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading itinerary:', error);
        return null;
    }
}

export async function customItineraryList() {
    try {
        const response = await limitedFetch(`http://localhost:8011/api/custom_itinerary/`); // Update the URL as necessary
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading itinerary:', error);
        return null;
    }
}

export async function customItineraryWIthParentList() {
    try {
        const response = await limitedFetch(`http://localhost:8011/api/itineraries/`); // Update the URL as necessary
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading itinerary:', error);
        return null;
    }
}
