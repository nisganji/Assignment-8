// Interactive 3D shapes using Three.js (no bundler required)
// This script creates a scene with a few basic shapes (cube, sphere, cone, plane) that float
// slowly and respond to hover and click. It loads Three.js from CDN dynamically if not present.

(function(){
    const THREE_CDN = 'https://unpkg.com/three@0.158.0/build/three.min.js';

    function loadScript(src) {
        return new Promise((resolve, reject) => {
            if (document.querySelector(`script[src="${src}"]`)) return resolve();
            const s = document.createElement('script');
            s.src = src;
            s.onload = () => resolve();
            s.onerror = () => reject(new Error('Failed to load ' + src));
            document.head.appendChild(s);
        });
    }

    function init() {
        const container = document.getElementById('three-container');
        if (!container) return;

        // Mobile fallback: if viewport is narrow, reduce pixel ratio and limit geometries
        const isMobile = window.matchMedia('(max-width: 600px)').matches;

        // Scene, camera, renderer
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 1.5, 5);

    const renderer = new THREE.WebGLRenderer({ antialias: !isMobile, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(isMobile ? Math.min(1, window.devicePixelRatio || 1) : (window.devicePixelRatio ? window.devicePixelRatio : 1));
        renderer.domElement.style.display = 'block';
        container.appendChild(renderer.domElement);

        // Lights
        const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.8);
        hemi.position.set(0, 1, 0);
        scene.add(hemi);

        const dir = new THREE.DirectionalLight(0xffffff, 0.6);
        dir.position.set(5, 10, 7.5);
        scene.add(dir);

    // Shapes container
        const shapes = [];

        // Helper: read CSS variable for tint, return THREE.Color
        function readShapeTint() {
            const s = getComputedStyle(document.documentElement).getPropertyValue('--shape-tint') || '#ffffff';
            return new THREE.Color(s.trim());
        }

        // Glass-like material factory (monochromatic translucent)
        function createGlassMaterial(baseColor) {
            const tint = readShapeTint();
            // blend base and tint
            const color = new THREE.Color(baseColor).lerp(tint, 0.6);
            return new THREE.MeshPhysicalMaterial({
                color: color,
                metalness: 0.0,
                roughness: 0.05,
                transparent: true,
                opacity: 0.6,
                transmission: 0.7, // glass-like
                clearcoat: 0.2,
                clearcoatRoughness: 0.1,
                reflectivity: 0.5
            });
        }

        // Add cube
        const cubeGeo = new THREE.BoxGeometry(0.9, 0.9, 0.9);
        const cube = new THREE.Mesh(cubeGeo, createGlassMaterial(0xffffff));
        cube.position.set(-2, 0.6, 0);
        scene.add(cube);
        shapes.push(cube);

        // Pyramid (cone with 4 radial segments)
        const coneGeo = new THREE.ConeGeometry(0.7, 1, 4);
        const cone = new THREE.Mesh(coneGeo, createGlassMaterial(0xffffff));
        cone.position.set(0, 0.6, -0.5);
        scene.add(cone);
        shapes.push(cone);

        // Rectangle (thin box)
        const rectGeo = new THREE.BoxGeometry(1.2, 0.6, 0.1);
        const rect = new THREE.Mesh(rectGeo, createGlassMaterial(0xffffff));
        rect.position.set(2, 0.6, 0.2);
        rect.rotation.set(0, 0.3, 0);
        scene.add(rect);
        shapes.push(rect);

        // Sphere
    const sphGeo = new THREE.SphereGeometry(0.5, isMobile ? 12 : 32, isMobile ? 12 : 32);
        const sphere = new THREE.Mesh(sphGeo, createGlassMaterial(0xffffff));
        sphere.position.set(-0.8, 2, -1);
        scene.add(sphere);
        shapes.push(sphere);

        // Pentagon (custom shape using Lathe or Extrude)
        const pentagonShape = new THREE.Shape();
        for (let i = 0; i < 5; i++) {
            const a = (i / 5) * Math.PI * 2 - Math.PI / 2;
            const r = 0.6;
            const x = Math.cos(a) * r;
            const y = Math.sin(a) * r;
            if (i === 0) pentagonShape.moveTo(x, y); else pentagonShape.lineTo(x, y);
        }
        pentagonShape.closePath();
    const pentGeo = new THREE.ExtrudeGeometry(pentagonShape, { depth: 0.2, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02 });
        const pent = new THREE.Mesh(pentGeo, createGlassMaterial(0xffffff));
        pent.position.set(-0.5, 0.9, 1);
        pent.rotation.set(-0.4, 0.2, 0);
        scene.add(pent);
        shapes.push(pent);

        // Star (5-point)
        const starShape = new THREE.Shape();
        const outer = 0.6, inner = 0.28;
        for (let i = 0; i < 10; i++) {
            const a = (i / 10) * Math.PI * 2 - Math.PI / 2;
            const r = i % 2 === 0 ? outer : inner;
            const x = Math.cos(a) * r;
            const y = Math.sin(a) * r;
            if (i === 0) starShape.moveTo(x, y); else starShape.lineTo(x, y);
        }
        starShape.closePath();
    const starGeo = new THREE.ExtrudeGeometry(starShape, { depth: 0.15, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.02 });
        const star = new THREE.Mesh(starGeo, createGlassMaterial(0xffffff));
        star.position.set(1.4, 1.2, -0.8);
        star.rotation.set(0.2, -0.3, 0.1);
        scene.add(star);
        shapes.push(star);

        // Prism (triangular prism)
        const prismShape = new THREE.Geometry();
        const p1 = new THREE.Vector3(-0.6, -0.3, 0);
        const p2 = new THREE.Vector3(0.6, -0.3, 0);
        const p3 = new THREE.Vector3(0, 0.6, 0);
        // front face
        prismShape.vertices.push(p1, p2, p3);
        prismShape.faces.push(new THREE.Face3(0,1,2));
        // back face (shift z)
        const p4 = p1.clone(); p4.z = -0.8;
        const p5 = p2.clone(); p5.z = -0.8;
        const p6 = p3.clone(); p6.z = -0.8;
        prismShape.vertices.push(p4, p5, p6);
        prismShape.faces.push(new THREE.Face3(3,5,4));
        // sides (simple)
        prismShape.faces.push(new THREE.Face3(0,3,4));
        prismShape.faces.push(new THREE.Face3(0,4,1));
        prismShape.faces.push(new THREE.Face3(1,4,5));
        prismShape.faces.push(new THREE.Face3(1,5,2));
        prismShape.faces.push(new THREE.Face3(2,5,3));
        prismShape.faces.push(new THREE.Face3(2,3,0));
        prismShape.computeFaceNormals();
    const prism = new THREE.Mesh(prismShape, createGlassMaterial(0xffffff));
        prism.position.set(0.8, 0.4, 1.2);
        prism.scale.set(0.8,0.8,0.8);
        scene.add(prism);
        shapes.push(prism);

        // Ground plane (transparent)
        const planeGeo = new THREE.PlaneGeometry(10, 10);
        const planeMat = new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0 });
        const plane = new THREE.Mesh(planeGeo, planeMat);
        plane.rotation.x = -Math.PI / 2;
        plane.position.y = 0;
        scene.add(plane);

        // Raycaster for hover/click
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        let hovered = null;

        // Accessibility: create invisible focusable elements that map to shapes so keyboard users can focus/click them
        const a11yContainer = document.createElement('div');
        a11yContainer.style.position = 'absolute';
        a11yContainer.style.left = '0';
        a11yContainer.style.top = '0';
        a11yContainer.style.width = '100%';
        a11yContainer.style.height = '100%';
        a11yContainer.style.pointerEvents = 'none';
        container.appendChild(a11yContainer);

        const a11yButtons = [];
        function createA11yButton(label, shape) {
            const btn = document.createElement('button');
            btn.className = 'sr-only';
            btn.type = 'button';
            btn.setAttribute('aria-label', label);
            btn.style.pointerEvents = 'auto';
            btn.addEventListener('focus', () => {
                hovered = shape;
                shape.material && shape.material.emissive && shape.material.emissive.setHex(0x222222);
                document.body.style.cursor = 'pointer';
            });
            btn.addEventListener('blur', () => {
                if (hovered === shape) {
                    hovered.material && hovered.material.emissive && hovered.material.emissive.setHex(0x000000);
                    hovered = null;
                    document.body.style.cursor = '';
                }
            });
            btn.addEventListener('click', () => {
                // replicate click pulse
                if (!shape) return;
                const initial = shape.scale.clone();
                const duration = 300;
                const start = performance.now();
                function pulse(now) {
                    const elapsed = now - start;
                    const progress = Math.min(elapsed / duration, 1);
                    const scale = 1 + 0.4 * Math.sin(Math.PI * progress);
                    shape.scale.set(initial.x * scale, initial.y * scale, initial.z * scale);
                    if (progress < 1) requestAnimationFrame(pulse);
                    else shape.scale.copy(initial);
                }
                requestAnimationFrame(pulse);
            });
            a11yContainer.appendChild(btn);
            a11yButtons.push(btn);
        }


        function onPointerMove(event) {
            const rect = renderer.domElement.getBoundingClientRect();
            mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        }

        function onClick(event) {
            if (!hovered) return;
            // simple scale pulse on click
            const target = hovered;
            const initial = target.scale.clone();
            const tl = {
                t: 0
            };
            const duration = 300; // ms
            const start = performance.now();
            function pulse(now) {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const scale = 1 + 0.4 * Math.sin(Math.PI * progress);
                target.scale.set(initial.x * scale, initial.y * scale, initial.z * scale);
                if (progress < 1) requestAnimationFrame(pulse);
                else target.scale.copy(initial);
            }
            requestAnimationFrame(pulse);
        }

        window.addEventListener('pointermove', onPointerMove);
        window.addEventListener('click', onClick);

        // Resize handling
        function onResize() {
            const w = container.clientWidth;
            const h = container.clientHeight;
            renderer.setSize(w, h);
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
        }
        window.addEventListener('resize', onResize);

        // Animation
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();

            // gentle floating and periodically update tint from CSS variable
            const tint = readShapeTint();
            shapes.forEach((s, i) => {
                s.rotation.x += 0.005 + i * 0.001;
                s.rotation.y += 0.01 + i * 0.001;
                s.position.y = (s.userData.baseY || s.position.y) + Math.sin(t * (0.5 + i * 0.1)) * 0.12 + (i === 3 ? 0.6 : 0);
                // gently lerp material color toward tint so shapes adapt dynamically
                if (s.material && s.material.color) {
                    s.material.color.lerp(tint, 0.02);
                }
            });

            // Hover detection
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(shapes, false);
            if (intersects.length > 0) {
                const obj = intersects[0].object;
                if (hovered !== obj) {
                    if (hovered) hovered.material.emissive && (hovered.material.emissive.setHex(0x000000));
                    hovered = obj;
                    hovered.material.emissive && hovered.material.emissive.setHex(0x222222);
                    // enlarge slightly
                    hovered.scale.set(1.12, 1.12, 1.12);
                    document.body.style.cursor = 'pointer';
                }
            } else {
                if (hovered) {
                    hovered.material.emissive && (hovered.material.emissive.setHex(0x000000));
                    hovered.scale.set(1,1,1);
                    hovered = null;
                    document.body.style.cursor = '';
                }
            }

            renderer.render(scene, camera);
        }

        animate();

        // Initial resize
        onResize();

        // After creating shapes, attach accessibility buttons mapping to each
        shapes.forEach((s, i) => {
            createA11yButton('Interactive shape ' + (i+1), s);
        });

        // expose a small API to update tint from outside
        window.__shapes_updateTint = function() {
            const tint = readShapeTint();
            shapes.forEach(s => {
                if (s.material && s.material.color) s.material.color.lerp(tint, 0.5);
            });
        };
    }

    loadScript(THREE_CDN).then(() => {
        // wait a tick for module availability
        setTimeout(init, 20);
    }).catch(err => {
        console.error('Could not load Three.js:', err);
    });
})();
