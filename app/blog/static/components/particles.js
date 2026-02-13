/**
 * Custom Animation Component Example
 * A simple canvas-based animation with no external dependencies
 * 
 * Usage in YAML:
 * - type: component
 *   id: particles
 *   script: static/components/particles.js
 *   data:
 *     count: 50
 *     color: "#e63946"
 *   caption: Interactive particle system
 */

(function() {
  const animations = document.querySelectorAll('[data-component-script*="particles"]');
  
  animations.forEach(container => {
    const config = JSON.parse(container.dataset.config || '{}');
    const numParticles = parseInt(config.count) || 50;
    const color = config.color || '#e63946';
    const width = parseInt(config.width) || 800;
    const height = parseInt(config.height) || 600;

    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    canvas.style.border = '2px solid #ccc';
    canvas.style.borderRadius = '8px';
    canvas.style.background = '#f5f5f5';
    container.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    
    // Particle system
    class Particle {
      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 2;
        this.vy = (Math.random() - 0.5) * 2;
        this.radius = Math.random() * 3 + 2;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
      }
    }

    const particles = Array.from({ length: numParticles }, () => new Particle());

    function animate() {
      ctx.clearRect(0, 0, width, height);
      
      particles.forEach(p => {
        p.update();
        p.draw();
      });

      // Draw connections
      ctx.strokeStyle = color;
      ctx.lineWidth = 0.5;
      ctx.globalAlpha = 0.2;

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 100) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }

      ctx.globalAlpha = 1;
      requestAnimationFrame(animate);
    }

    animate();
  });
})();
