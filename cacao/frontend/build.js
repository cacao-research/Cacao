const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const distDir = path.join(__dirname, 'dist');

// Ensure dist exists
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

console.log('[Cacao] Building frontend...');

// Build full CSS (backward compat)
console.log('[Cacao] Compiling LESS → CSS (full bundle)');
execSync('npx lessc src/styles/index.less dist/cacao.css', {
  cwd: __dirname,
  stdio: 'inherit'
});

// Build category CSS files for optimized loading
const categories = ['core', 'cat-layout', 'cat-display', 'cat-typography', 'cat-form', 'cat-charts'];
console.log('[Cacao] Compiling category CSS:', categories.join(', '));
for (const cat of categories) {
  execSync(`npx lessc src/styles/${cat}.less dist/cacao-${cat}.css`, {
    cwd: __dirname,
    stdio: 'inherit'
  });
}

// Build JS
// Note: Don't use --global-name because window.Cacao is set manually in the code
console.log('[Cacao] Bundling JS');
execSync('npx esbuild src/components/index.js --bundle --outfile=dist/cacao.js --format=iife --external:React --external:ReactDOM --external:Chart', {
  cwd: __dirname,
  stdio: 'inherit'
});

console.log('[Cacao] Build complete!');
