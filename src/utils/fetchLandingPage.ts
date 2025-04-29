export async function fetchLandingPage(id: number) {
    const response = await fetch(`http://127.0.0.1:8011/api/landingpage/${id}/`);
    if (!response.ok) {
        throw new Error(`Failed to fetch landing page: ${response.status}`);
    }
    const data = await response.json();
    return data;
}
