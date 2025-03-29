// src/utils/limitedFetch.ts

import pLimit from 'p-limit';

// Define the concurrency limit (e.g., 5 concurrent requests)
const limit = pLimit(5);

/**
 * Centralized throttled fetch function.
 * @param input - The resource that you wish to fetch.
 * @param init - An options object containing any custom settings.
 * @returns A Promise that resolves to the Response.
 */
export async function limitedFetch(input: RequestInfo, init?: RequestInit): Promise<Response> {
    return limit(() => fetch(input, init));
}
