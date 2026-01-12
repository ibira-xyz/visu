# Interactive Component System

## Overview

A flexible system for embedding interactive JavaScript animations and visualizations into blog posts. Components are defined in the post's YAML metadata alongside markdown content and images, with complete separation between component logic (JavaScript) and content structure.

## Architecture

### 1. **YAML Definition** (Post Metadata)
Components are declared in the `content_metadata` array like other content types:

```yaml
content_metadata:
  - type: markdown
    path: static/assets/intro.md
  
  - type: component
    id: my-animation
    script: static/components/my-component.js
    data:
      param1: value1
      param2: value2
    caption: Optional description of the component
  
  - type: image
    path: static/assets/image.png
```

### 2. **Controller Processing** (`controllers/post_controller.py`)
- Parses component entries from YAML
- Creates HTML container `<div>` with:
  - Unique `id` attribute
  - `data-component-script` pointing to JavaScript file
  - Custom `data-*` attributes for configuration
- Collects script paths for loading

### 3. **Template Rendering** (`templates/post.html`)
- Inserts component containers in content flow
- Loads component scripts at end of article
- Scripts execute when DOM is ready

### 4. **Component Scripts** (`static/components/*.js`)
- Self-contained JavaScript files
- Find their container via `id`
- Read configuration from `data-*` attributes
- Create and manage their own DOM elements/canvas
- Handle external library loading if needed

## Usage

### Basic Example

**1. Create component JavaScript** (`static/components/hello.js`):
```javascript
(function() {
  const containers = document.querySelectorAll('[data-component-script*="hello"]');
  
  containers.forEach(container => {
    const config = window.getComponentConfig(container.id);
    const message = config.message || 'Hello World';
    
    const div = document.createElement('div');
    div.textContent = message;
    div.style.fontSize = '24px';
    div.style.textAlign = 'center';
    container.appendChild(div);
  });
})();
```

**2. Add to post YAML**:
```yaml
content_metadata:
  - type: component
    id: greeting
    script: static/components/hello.js
    data:
      message: "Welcome to my blog!"
    caption: A simple greeting component
```

### Physics Simulation Example

**YAML:**
```yaml
content_metadata:
  - type: component
    id: pendulum-sim
    script: static/components/pendulum.js
    data:
      length: 200
      angle: 60
      width: 800
      height: 600
    caption: Simple pendulum demonstrating harmonic motion
```

The `pendulum.js` script loads Matter.js dynamically and creates the simulation.

### Custom Canvas Animation

**YAML:**
```yaml
content_metadata:
  - type: component
    id: particles
    script: static/components/particles.js
    data:
      count: 100
      color: "#e63946"
    caption: Interactive particle system
```

## Included Examples

### 1. Pendulum (`components/pendulum.js`)
Physics-based pendulum using Matter.js

**Parameters:**
- `length` - Rope length in pixels (default: 200)
- `angle` - Initial angle in degrees (default: 45)
- `width` - Canvas width (default: 800)
- `height` - Canvas height (default: 600)

### 2. Particles (`components/particles.js`)
Particle system with no dependencies

**Parameters:**
- `count` - Number of particles (default: 50)
- `color` - Particle color (default: #e63946)
- `width` - Canvas width (default: 800)
- `height` - Canvas height (default: 600)

## Creating Custom Components

### Template Structure

```javascript
(function() {
  // Find all instances of this component type
  const components = document.querySelectorAll('[data-component-script*="your-component"]');
  
  components.forEach(container => {
    // Get configuration
    const config = window.getComponentConfig(container.id);
    const param1 = config.param1 || 'default';
    
    // Create your visualization
    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 600;
    container.appendChild(canvas);
    
    // Your animation logic here
    const ctx = canvas.getContext('2d');
    function animate() {
      // Draw frame
      requestAnimationFrame(animate);
    }
    animate();
  });
})();
```

### Loading External Libraries

Components can load dependencies dynamically:

```javascript
if (typeof ThirdPartyLib === 'undefined') {
  const script = document.createElement('script');
  script.src = 'https://cdn.example.com/library.js';
  script.onload = initComponent;
  document.head.appendChild(script);
} else {
  initComponent();
}
```

### Accessing Configuration

Use the helper function to get all data attributes:

```javascript
const config = window.getComponentConfig(container.id);
// Returns: { param1: 'value1', param2: 'value2', ... }
```

## Files Modified

### Core System
- `/src/controllers/post_controller.py` - Added component type handler
- `/src/templates/post.html` - Added script loading
- `/src/static/styles.css` - Added component styling
- `/src/templates/base.html` - Added component-loader.js

### Created
- `/src/static/component-loader.js` - Utility functions
- `/src/static/components/` - Component directory
- `/src/static/components/pendulum.js` - Example physics component
- `/src/static/components/particles.js` - Example custom animation

## Benefits of This Approach

1. **Separation of Concerns**: Content structure (YAML) separate from behavior (JS)
2. **Flexibility**: Any JavaScript animation/visualization can be a component
3. **Reusability**: Same component script can be used multiple times with different configs
4. **No Markdown Pollution**: Keep markdown clean, components in metadata
5. **Progressive Enhancement**: Page works without JS, components enhance when loaded
6. **Easy Testing**: Test components independently in HTML files

## Component Guidelines

### Best Practices

1. **Self-contained**: Don't pollute global namespace (use IIFE)
2. **Defensive**: Check if dependencies are loaded
3. **Configurable**: Read settings from data attributes
4. **Responsive**: Support different sizes via config
5. **Clean up**: Remove event listeners if needed

### Performance Tips

- Limit number of components per post (2-3 heavy animations)
- Use `requestAnimationFrame` for animations
- Implement pause/play for off-screen components
- Lazy-load heavy libraries only when needed

## Troubleshooting

**Component not appearing:**
- Check `id` is unique
- Verify `script` path is correct
- Check browser console for errors
- Ensure component script selector matches filename

**Configuration not working:**
- Data attribute names are lowercase in HTML
- Use `window.getComponentConfig()` to access
- Check YAML indentation under `data:`

**Script loading issues:**
- Scripts load after DOM content
- External libraries might need onload callbacks
- Check CDN URLs are accessible

## Future Enhancements

Potential additions:
- Component hot-reloading in development
- Built-in playback controls (pause/play/reset)
- Component marketplace/gallery
- TypeScript support for components
- WebGL/Three.js helper utilities
- Data binding from backend APIs
