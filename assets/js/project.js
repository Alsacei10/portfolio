/* 项目详情页：读取 ?id= 参数，从 data/projects.json 渲染单个项目 */
(function () {
  'use strict';

  var DATA_URL = 'data/projects.json';

  function $(id) { return document.getElementById(id); }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function getProjectId() {
    var params = new URLSearchParams(window.location.search);
    return params.get('id') || '';
  }

  function loadData() {
    return fetch(DATA_URL, { cache: 'no-store' })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .catch(function (err) {
        console.error('[portfolio] 数据加载失败：', err);
        return null;
      });
  }

  function render(project, index, projects) {
    document.title = (project.title || '项目详情') + ' · 戴章勇作品集';

    fillMeta(project);
    fillSummary(project);
    fillDocs(project);
    fillGallery(project);
    fillPager(index, projects);

    if (window.Lightbox) window.Lightbox.init();
  }

  function fillMeta(project) {
    $('p-title').textContent = project.title || '';
    $('p-tagline').textContent = project.tagline || '';

    var chips = [];
    if (project.role) chips.push({ label: '我的角色', value: project.role });
    if (project.period) chips.push({ label: '项目周期', value: project.period });
    var html = chips.map(function (c) {
      return '<span class="meta-chip"><b>' + escapeHtml(c.label) + '</b>' + escapeHtml(c.value) + '</span>';
    }).join('');
    html += (project.tags || []).map(function (t) {
      return '<span class="tag">' + escapeHtml(t) + '</span>';
    }).join('');
    $('p-meta').innerHTML = html;
  }

  function fillSummary(project) {
    var summary = $('p-summary');
    summary.innerHTML = (project.summary || []).map(function (p) {
      return '<p>' + escapeHtml(p) + '</p>';
    }).join('');
  }

  function fillDocs(project) {
    var actions = $('p-doc-actions');
    var note = $('p-doc-note');
    var html = '';

    if (project.prdPdf) {
      html += '<a class="btn btn-primary" href="' + escapeHtml(project.prdPdf) + '" target="_blank" rel="noopener">查看 PRD</a>';
      html += '<a class="btn btn-secondary" href="' + escapeHtml(project.prdPdf) + '" download="' + escapeHtml((project.title || '项目') + '-PRD.pdf') + '">下载 PRD</a>';
      if (note) note.textContent = '提示：若 PDF 无法在浏览器内直接预览，请使用「下载 PRD」按钮。';
    }
    var proto = project.links && project.links.prototype;
    if (proto) {
      html += '<a class="btn btn-secondary" href="' + escapeHtml(proto) + '" target="_blank" rel="noopener">在线原型</a>';
    }
    actions.innerHTML = html;
  }

  function fillGallery(project) {
    var gallery = $('p-gallery');
    var images = project.images || [];
    if (!images.length) {
      gallery.innerHTML = '<p class="section-sub">暂无原型图。</p>';
      return;
    }
    gallery.innerHTML = images.map(function (src, i) {
      var alt = (project.title || '项目') + ' 界面示意 ' + (i + 1);
      return (
        '<figure>' +
          '<img src="' + escapeHtml(src) + '" alt="' + escapeHtml(alt) + '" loading="lazy" ' +
          'data-lightbox data-caption="' + escapeHtml(alt) + '">' +
          '<figcaption>界面示意 ' + (i + 1) + '</figcaption>' +
        '</figure>'
      );
    }).join('');
  }

  function fillPager(index, projects) {
    var pager = $('pager');
    if (!pager || projects.length < 2) return;
    var prev = projects[(index - 1 + projects.length) % projects.length];
    var next = projects[(index + 1) % projects.length];
    pager.innerHTML =
      '<a class="prev" href="project.html?id=' + encodeURIComponent(prev.id) + '">&larr; ' + escapeHtml(prev.title) + '</a>' +
      '<a class="next" href="project.html?id=' + encodeURIComponent(next.id) + '">' + escapeHtml(next.title) + ' &rarr;</a>';
  }

  function renderMissing(id) {
    $('p-title').textContent = '未找到该项目';
    $('p-tagline').textContent = id ? '项目「' + id + '」不存在或已被移除。' : '缺少项目 ID 参数（?id=xxx）。';
    var actions = $('p-doc-actions');
    actions.innerHTML = '<a class="btn btn-primary" href="index.html#projects">返回作品列表</a>';
    var section = $('gallery-section');
    if (section) section.style.display = 'none';
  }

  function renderError() {
    $('p-title').textContent = '数据加载失败';
    $('p-tagline').textContent = '请通过本地服务器访问（如 python -m http.server 8000）或部署后再打开本页。';
    var actions = $('p-doc-actions');
    actions.innerHTML = '<a class="btn btn-primary" href="index.html">返回首页</a>';
    var section = $('gallery-section');
    if (section) section.style.display = 'none';
  }

  function init() {
    var year = $('footer-year');
    if (year) year.textContent = String(new Date().getFullYear());

    var id = getProjectId();
    loadData().then(function (data) {
      if (!data) { renderError(); return; }
      if (data.profile && data.profile.name) $('nav-name').textContent = data.profile.name;
      var projects = data.projects || [];
      var index = -1;
      for (var i = 0; i < projects.length; i++) {
        if (projects[i].id === id) { index = i; break; }
      }
      if (index === -1) { renderMissing(id); return; }
      render(projects[index], index, projects);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
