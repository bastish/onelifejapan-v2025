import type { Attributes } from 'astro-embed-components-in-content';
import { parseDynamicContent, addUidsToContents } from 'astro-embed-components-in-content';
import {
    dynamicConfig,
    allowedConfig,
    allowedDynamicComponents,
} from './astroEmbedComponentsConfig';

// @ts-ignore
import AstroEmbedComponents from './AstroEmbedComponents.astro';
export { AstroEmbedComponents };

/**
 * Represents an entry for a dynamic component with its corresponding properties.
 */
interface ComponentEntry {
    Component: any;
    componentProps: Attributes;
}

/**
 * Embeds dynamic components in the provided content.
 *
 * - Adds unique IDs to content based on allowed configurations.
 * - Parses the content for each allowed component.
 * - Collects and appends parsed components to the aecComponents array.
 *
 * @param {ComponentEntry[]} aecComponents - Array to store dynamic components.
 * @param {string} content - Content to parse for dynamic components.
 * @returns {[ComponentEntry[], string]} - Updated aecComponents array and content.
 */
export const embedComponents = (
    aecComponents: ComponentEntry[],
    content: string
): [ComponentEntry[], string] => {
    // Add unique IDs to content based on allowed configurations
    const updatedContent = addUidsToContents(allowedConfig, content) as string;

    // Array to hold parsed components
    const allParsedComponents: Attributes[] = [];

    // Parse content for each allowed component
    Object.keys(allowedDynamicComponents).forEach((componentName) => {
        const config = dynamicConfig(componentName);
        const parsedComponents = parseDynamicContent([updatedContent], config);

        // Collect parsed components
        allParsedComponents.push(...parsedComponents);
    });

    // Append parsed components to aecComponents array
    allParsedComponents.forEach((parsed: Attributes) => {
        const Component = allowedDynamicComponents[parsed.componentName];
        if (Component) {
            aecComponents.push({ Component, componentProps: parsed });
        }
    });

    return [aecComponents, updatedContent];
};

/**
 * Usage:
 *
 * 1. Import Required Modules:
 *    import { embedComponents } from '../astroEmbedComponent/embedComponents';
 *    import AstroEmbedComponent from 'src/astroEmbedComponent/AstroEmbedComponents.astro';
 *
 * 2. Initialize and Process Content:
 *    let aecComponents: ComponentEntry[] = [];
 *    [aecComponents, data.content1] = embedComponents(aecComponents, data.content1);
 *    [aecComponents, data.content2] = embedComponents(aecComponents, data.content2);
 *
 * 3. Render Dynamic Components:
 *    <AstroEmbedComponent aecComponents={aecComponents} />
 *
 * Notes:
 * - Ensure that the components listed in your configuration (e.g., `allowedDynamicComponents`)
 *   are correctly imported and available within your project structure.
 * - Adjust the import paths (`'../astroEmbedComponent/embedComponents'` and
 *   `'src/astroEmbedComponent/AstroEmbedComponents.astro'`) to match your project’s file structure.
 */
