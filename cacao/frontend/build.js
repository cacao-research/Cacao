const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const distDir = path.join(__dirname, 'dist');

// Ensure dist exists
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

console.log('[Cacao] Building frontend...');

// Build CSS
console.log('[Cacao] Compiling LESS → CSS');
execSync('npx lessc src/styles/index.less dist/cacao.css', {
  cwd: __dirname,
  stdio: 'inherit'
});

// Build JS
console.log('[Cacao] Bundling JS');
execSync('npx esbuild src/components/index.js --bundle --outfile=dist/cacao.js --format=iife --global-name=Cacao --external:React --external:ReactDOM --external:Chart', {
  cwd: __dirname,
  stdio: 'inherit'
});

console.log('[Cacao] Build complete!');
