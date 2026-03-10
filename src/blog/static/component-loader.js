/**
 * Interactive Component Loader
 * Automatically initializes components on page load
 */

document.addEventListener('DOMContentLoaded', () => {
  // Find all component containers
  const components = document.querySelectorAll('[data-component-script]');
  
  components.forEach(container => {
    const componentId = container.id;
    console.log(`Component container ready: ${componentId}`);
    
    // Components can access their container via document.getElementById(componentId)
    // and read any data-* attributes for configuration
  });
});

// Utility function for components to get their configuration
window.getComponentConfig = function(componentId) {
  const container = document.getElementById(componentId);
  if (!container) return {};
  
  const config = {};
  // Extract all data-* attributes
  for (const attr of container.attributes) {
    if (attr.name.startsWith('data-') && attr.name !== 'data-component-script') {
      const key = attr.name.substring(5); // Remove 'data-' prefix
      config[key] = attr.value;
    }
  }
  return config;
};
