import type { DelimitersMap, ComponentConfig, AllowedConfig } from 'astro-embed-components-in-content';

/**
 * This file is a template for setting up dynamic component configurations.
 * Replace the example components with your actual components, adjusting the imports
 * and configuration objects as needed.
 */

/**
 * Example imports for dynamically embedded components.
 * Replace these imports with the actual components from your project.
 *
 * Uncomment the following lines and replace the paths with actual paths to your components:
 *
 * // import ExampleComponent from '../components/ExampleComponent.astro';
 * // import ExampleComponent2 from '../components/ExampleComponent2.astro';
 */
// Add more imports as needed...

/**
 * Maps component names to their corresponding Astro component implementations.
 * Ensures only allowed components can be dynamically rendered based on their names.
 */

//import SingleImageSlider from '../components/SingleImageSlider.astro';
import SingleImageSlider from '../components/SingleImageSlider.astro';
import ResponsiveFramedFloatingImage from '..//components/ResponsiveFramedFloatingImage.astro';
export const allowedDynamicComponents: Record<string, any> = {
    ResponsiveFramedFloatingImage, // Add your components here
    SingleImageSlider,
    // ExampleComponent2,
    // Add more components as needed...
};

/**
 * Defines available delimiters for identifying dynamic components within content.
 * Customize these delimiters as needed to avoid conflicts with other content.
 */
export const delimiters: DelimitersMap = {
    curly: { start: '{', end: '}' },
    square: { start: '[', end: ']' },
};

// Common properties for all components
const baseProps = ['aecuid', 'id'];
const exampleProps = ['src', 'alt', 'width', 'height', 'float']; // Replace with your component's specific properties

const imageProps = ['src', 'width', 'height', 'alt', 'float'];
// Default delimiters if not specified by the component
const defaultDelimiter = delimiters.curly;

/**
 * Configuration for each allowed component, specifying properties and delimiters.
 * Adjust the configuration below based on your components' requirements.
 */
const config: { [key: string]: ComponentConfig } = {
    ResponsiveFramedFloatingImage: {
        component: 'ResponsiveFramedFloatingImage',
        allowedProps: [...baseProps, ...imageProps, 'srcLarge', 'srcMedium', 'srcSmall', 'altText'],
        delimiters: delimiters.curly,
    },
    SingleImageSlider: {
        component: 'SingleImageSlider',
        allowedProps: [...baseProps, 'compiled_image', 'height', 'width', 'float'],
        delimiters: delimiters.curly,
    },
    // ExampleComponent2: {
    //     component: 'ExampleComponent2',
    //     allowedProps: [...baseProps, ...exampleProps, 'text', 'someOtherProp'],
    //     delimiters: delimiters.curly,
    // },
    // Add more component configurations here...
};

// Generate a list of component names from the config object
const keys = Object.keys(config);

/**
 * Generates an allowedConfig object for validating component usage.
 * Provides a quick reference for component names and their delimiters.
 */
export const allowedConfig: AllowedConfig = {
    componentNames: keys.reduce(
        (acc, key) => {
            acc[key] = config[key].component;
            return acc;
        },
        {} as { [key: string]: string },
    ),
    delimiters: delimiters,
};

/**
 * Retrieves the configuration for a specific component by name.
 * Returns a default configuration if the component is not found.
 *
 * @param {string} componentName - The name of the component.
 * @returns {ComponentConfig} - The configuration object for the component.
 */
export const dynamicConfig = (componentName: string): ComponentConfig => {
    return (
        config[componentName] || {
            component: componentName,
            allowedProps: [],
            delimiters: defaultDelimiter,
        }
    );
};
