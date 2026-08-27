#!/usr/bin/env node
// 内容校验脚本：检查 data/projects.json 引用的素材文件是否都存在、字段是否完整
// 运行：node scripts/check-content.js
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA_PATH = path.join(ROOT, 'data', 'projects.json');

let data;
try {
  data = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
} catch (e) {
  console.error('✖ 无法解析 data/projects.json：' + e.message);
  process.exit(1);
}

const problems = [];
let checked = 0;

function checkFile(rel) {
  if (!rel) return;
  checked += 1;
  if (!fs.existsSync(path.join(ROOT, rel))) {
    problems.push('缺少文件：' + rel);
  }
}

const profile = data.profile || {};
if (!profile.name) problems.push('profile：缺少 name');
checkFile(profile.avatar);
checkFile(profile.resumePdf);

const projects = Array.isArray(data.projects) ? data.projects : [];
if (projects.length === 0) {
  problems.push('projects 为空数组，请至少添加一个项目');
}

const seen = new Set();
projects.forEach(function (p, i) {
  const label = '项目[' + i + '] ' + (p.id || '(无 id)');
  ['id', 'title', 'tagline', 'role', 'period', 'cover'].forEach(function (k) {
    if (p[k] === undefined || p[k] === '') problems.push(label + '：缺少字段 ' + k);
  });
  if (!Array.isArray(p.images) || p.images.length === 0) {
    problems.push(label + '：images 为空');
  }
  if (p.id && seen.has(p.id)) problems.push('项目 id 重复：' + p.id);
  seen.add(p.id);
  checkFile(p.cover);
  if (p.prdPdf) checkFile(p.prdPdf);
  (p.images || []).forEach(function (im) {
    if (typeof im === 'string') checkFile(im);
    else if (im && im.src) checkFile(im.src);
    else problems.push(label + '：images 中存在无效项');
  });
});

if (problems.length > 0) {
  console.error('✖ 检查未通过（' + problems.length + ' 个问题）：');
  problems.forEach(function (p) { console.error('  - ' + p); });
  process.exit(1);
}

console.log('✓ 内容检查通过：' + projects.length + ' 个项目，' + checked + ' 个素材文件均存在');
