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

console.log(import.meta.env);
export const baseHost = `http://${import.meta.env.DEV_HOST}:3020`;
