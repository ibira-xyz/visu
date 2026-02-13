/**
 * Pendulum Animation Component
 * A simple physics pendulum using Matter.js
 * 
 * Usage in YAML:
 * - type: component
 *   id: my-pendulum
 *   script: static/components/pendulum.js
 *   data:
 *     length: 200
 *     angle: 45
 *   caption: A swinging pendulum
 */

(function() {
  // Load Matter.js if not already loaded
  if (typeof Matter === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js';
    script.onload = initPendulum;
    document.head.appendChild(script);
  } else {
    initPendulum();
  }

  function initPendulum() {
    // Find all pendulum components
    const pendulums = document.querySelectorAll('[data-component-script*="pendulum"]');
    
    pendulums.forEach(container => {
      const config = window.getComponentConfig(container.id);
      const width = parseInt(config.width) || 800;
      const height = parseInt(config.height) || 600;
      const length = parseInt(config.length) || 200;
      const angle = (parseInt(config.angle) || 45) * Math.PI / 180;

      // Create canvas
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      canvas.style.border = '2px solid #ccc';
      canvas.style.borderRadius = '8px';
      container.appendChild(canvas);

      // Setup Matter.js
      const engine = Matter.Engine.create();
      const render = Matter.Render.create({
        canvas: canvas,
        engine: engine,
        options: {
          width: width,
          height: height,
          wireframes: false,
          background: '#f5f5f5'
        }
      });

      // Create pendulum
      const anchorX = width / 2;
      const anchorY = 100;
      const bobX = anchorX + Math.sin(angle) * length;
      const bobY = anchorY + Math.cos(angle) * length;

      const anchor = Matter.Bodies.circle(anchorX, anchorY, 10, {
        isStatic: true,
        render: { fillStyle: '#333' }
      });

      const bob = Matter.Bodies.circle(bobX, bobY, 30, {
        density: 0.04,
        frictionAir: 0.005,
        render: { fillStyle: '#e63946' }
      });

      const constraint = Matter.Constraint.create({
        bodyA: anchor,
        bodyB: bob,
        length: length,
        stiffness: 1,
        render: { strokeStyle: '#333', lineWidth: 2 }
      });

      Matter.World.add(engine.world, [anchor, bob, constraint]);
      Matter.Render.run(render);
      Matter.Runner.run(Matter.Runner.create(), engine);
    });
  }
})();
