/* 首页：从 data/projects.json 读取个人资料与项目列表并渲染 */
(function () {
  'use strict';

  var DATA_URL = 'data/projects.json';

  function $(id) { return document.getElementById(id); }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function fill(id, value) {
    var el = $(id);
    if (el && value !== undefined && value !== null) el.textContent = value;
  }

  function showError(msg) {
    var el = $('data-error');
    if (el) {
      if (msg) el.textContent = msg;
      el.classList.add('show');
    }
  }

  function loadData() {
    return fetch(DATA_URL, { cache: 'no-store' })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .catch(function (err) {
        console.error('[portfolio] 数据加载失败：', err);
        showError();
        return null;
      });
  }

  function renderProfile(profile) {
    fill('nav-name', profile.name);
    fill('hero-name', profile.name);
    fill('hero-role', profile.role);
    fill('hero-tagline', profile.tagline);
    fill('footer-name', profile.name);
    fill('skills-label', profile.skillsLabel || '技能与工具');

    var avatar = $('avatar');
    if (avatar && profile.avatar) avatar.src = profile.avatar;

    var resume = profile.resumePdf || 'assets/resume.pdf';
    var navResume = $('nav-resume'), heroResume = $('hero-resume');
    if (navResume) navResume.href = resume;
    if (heroResume) heroResume.href = resume;

    var bio = $('about-bio');
    if (bio && Array.isArray(profile.bio)) {
      bio.innerHTML = profile.bio.map(function (p) { return '<p>' + escapeHtml(p) + '</p>'; }).join('');
    }

    var skillList = $('skill-list');
    if (skillList && Array.isArray(profile.skills)) {
      skillList.innerHTML = profile.skills.map(function (s) {
        return '<span class="skill-item">' + escapeHtml(s) + '</span>';
      }).join('');
    }

    var email = $('contact-email');
    if (email && profile.email) {
      email.textContent = profile.email;
      email.href = 'mailto:' + profile.email;
    }
    fill('contact-wechat', profile.wechat);
    var wechatLine = $('contact-wechat-line');
    if (wechatLine) wechatLine.style.display = profile.wechat ? '' : 'none';
  }

  function renderProjects(projects) {
    var grid = $('project-grid');
    if (!grid) return;
    if (!Array.isArray(projects) || projects.length === 0) {
      grid.innerHTML = '<p class="section-sub">暂无作品，敬请期待。</p>';
      return;
    }
    grid.innerHTML = projects.map(function (p) {
      var tags = (p.tags || []).map(function (t) {
        return '<span class="tag">' + escapeHtml(t) + '</span>';
      }).join('');
      return (
        '<a class="card" href="project.html?id=' + encodeURIComponent(p.id) + '">' +
          '<img class="card-cover" src="' + escapeHtml(p.cover || '') + '" alt="' + escapeHtml(p.title || '') + ' 封面" loading="lazy">' +
          '<div class="card-body">' +
            '<h3 class="card-title">' + escapeHtml(p.title || '') + '</h3>' +
            '<p class="card-tagline">' + escapeHtml(p.tagline || '') + '</p>' +
            (tags ? '<div class="card-tags">' + tags + '</div>' : '') +
            '<span class="card-foot">查看详情 <span class="arrow">&rarr;</span></span>' +
          '</div>' +
        '</a>'
      );
    }).join('');
  }

  function init() {
    var year = $('footer-year');
    if (year) year.textContent = String(new Date().getFullYear());

    loadData().then(function (data) {
      if (!data) return;
      if (data.profile) renderProfile(data.profile);
      renderProjects(data.projects);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
