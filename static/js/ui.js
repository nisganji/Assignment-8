// UI utilities: dynamic background gradient and theme toggle
(function(){
    function randInt(min,max){return Math.floor(Math.random()*(max-min+1))+min}
    function randomHue(){return randInt(0,359)}

    // complementary hues: pick hue1 and hue2 = hue1 + 180 mod 360
    function hueToHsl(h, s=70, l=50){ return `hsl(${h} ${s}% ${l}%)`; }

    function setBackgroundColors(){
        const h1 = randomHue();
        const h2 = (h1 + 180) % 360;
        // slightly vary saturation/lightness for pleasing combos
        const c1 = hueToHsl(h1, 68, 46);
        const c2 = hueToHsl(h2, 65, 42);
        document.documentElement.style.setProperty('--bg1', c1);
        document.documentElement.style.setProperty('--bg2', c2);
        // set a derived shape tint (midpoint blended) for shapes
        // convert hsl to rgb via CSS compute: create element
        const tmp = document.createElement('div');
        tmp.style.color = `linear-gradient(${c1}, ${c2})`;
        // instead approximate with midpoint hue
        const midHue = (h1 + 90) % 360;
        const tint = `hsl(${midHue} 40% 70%)`;
        document.documentElement.style.setProperty('--shape-tint', tint);
        // notify shapes to update tint if available
        if (window.__shapes_updateTint) window.__shapes_updateTint();
    }

    // toggle dark/light
    function applyTheme(theme){
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }

    function initThemeToggle() {
        const toggle = document.getElementById('theme-toggle');
        if (!toggle) return;
        const saved = localStorage.getItem('theme') || 'auto';
        if (saved === 'auto') {
            const prefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            applyTheme(prefers);
        } else applyTheme(saved);

        toggle.addEventListener('change', (e) => {
            const val = e.target.value;
            if (val === 'auto') {
                const prefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                applyTheme(prefers);
                localStorage.setItem('theme', 'auto');
            } else applyTheme(val);
        });
    }

    // On load
    document.addEventListener('DOMContentLoaded', () => {
        setBackgroundColors();
        initThemeToggle();
        // animate background shift slightly
        const root = document.documentElement;
        root.style.setProperty('--bg-anim', '0%');
        setTimeout(()=> root.style.setProperty('--bg-anim','100%'), 50);
    });
})();
