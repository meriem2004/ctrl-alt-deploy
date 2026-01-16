#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Determine paths
const projectRoot = path.resolve(__dirname, '..');
const srcCli = path.join(projectRoot, 'src', 'cli.py');

// Try to find the virtual environment python
const venvPythonWin = path.join(projectRoot, 'venv', 'Scripts', 'python.exe');
const venvPythonUnix = path.join(projectRoot, 'venv', 'bin', 'python');

let pythonPath = 'python'; // Default fallback

if (process.platform === 'win32' && fs.existsSync(venvPythonWin)) {
  pythonPath = venvPythonWin;
} else if (fs.existsSync(venvPythonUnix)) {
  pythonPath = venvPythonUnix;
}

// Arguments passed to this script
const args = process.argv.slice(2);

console.log(`🚀 Deployment Automation (Wrapper)`);
// console.log(`Debug: Using Python at: ${pythonPath}`);

const child = spawn(pythonPath, [srcCli, ...args], {
  stdio: 'inherit',
  cwd: projectRoot,
  shell: false
});

child.on('exit', (code) => {
  process.exit(code);
});
