export function convertLineBreaksToParagraphs(text: string | undefined) {
    if (typeof text !== 'string') {
        return '';
    }
    const normalizedText = text.replace(/\r\n/g, '\n');
    return normalizedText
        .split('\n\n')
        .map((paragraph) => `<p>${paragraph}</p>`)
        .join('');
}

export const baseHost = `http://${import.meta.env.DEV_HOST}:3020`;

export function hasProperty(obj: any, ...propertyPaths: string[]) {
    if (!obj) return false;
    for (let propertyPath of propertyPaths) {
        const properties = propertyPath.split('.');
        let current = obj;
        for (let property of properties) {
            if (!current[property]) {
                current = null;
                break;
            }
            current = current[property];
        }
        if (current && (Array.isArray(current) ? current.length > 0 : Object.keys(current).length > 0)) {
            return true;
        }
    }
    return false;
}

/**
 * Strips <p> and <em> HTML tags from the provided string.
 * @param input - The string that may contain HTML tags.
 * @returns The string with <p> and <em> tags removed.
 */
export function stripSimpleHtmlTags(input: string): string {
    return input.replace(/<\/?(p|em)[^>]*>/gi, '');
}
