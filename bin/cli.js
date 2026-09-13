#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const targetSkillDir = path.join(os.homedir(), '.gemini', 'config', 'skills', 'remote-control-loop');

console.log('🚀 Installing Antigravity Remote Control Skill...');

function copyRecursiveSync(src, dest) {
    const exists = fs.existsSync(src);
    const stats = exists && fs.statSync(src);
    const isDirectory = exists && stats.isDirectory();

    if (isDirectory) {
        if (!fs.existsSync(dest)) {
            fs.mkdirSync(dest, { recursive: true });
        }
        fs.readdirSync(src).forEach((childItemName) => {
            copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
        });
    } else {
        fs.copyFileSync(src, dest);
    }
}

try {
    const pkgRoot = path.join(__dirname, '..');
    copyRecursiveSync(path.join(pkgRoot, 'SKILL.md'), path.join(targetSkillDir, 'SKILL.md'));
    copyRecursiveSync(path.join(pkgRoot, 'scripts'), path.join(targetSkillDir, 'scripts'));

    console.log(`✅ Skill successfully installed to: ${targetSkillDir}`);
    console.log(`💡 You can now tell Antigravity: "Bật remote" or "Kích hoạt remote skill"!`);
} catch (err) {
    console.error(`❌ Failed to install skill:`, err.message);
    process.exit(1);
}
