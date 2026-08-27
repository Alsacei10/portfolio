/* 极简 Lightbox：点击 [data-lightbox] 图片放大，支持左右切换与键盘操作 */
(function () {
  'use strict';

  var lightbox = null, img = null, caption = null;
  var images = [];
  var current = 0;

  function isOpen() {
    return lightbox && lightbox.classList.contains('open');
  }

  function update() {
    var el = images[current];
    if (!el) return;
    img.src = el.currentSrc || el.src;
    img.alt = el.alt || '';
    caption.textContent = el.getAttribute('data-caption') || '';
  }

  function open(index) {
    if (!images.length || !lightbox) return;
    current = index;
    update();
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    if (!lightbox) return;
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  function step(delta) {
    if (!images.length) return;
    current = (current + delta + images.length) % images.length;
    update();
  }

  function init() {
    lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    img = document.getElementById('lb-img');
    caption = document.getElementById('lb-caption');
    var prevBtn = document.getElementById('lb-prev');
    var nextBtn = document.getElementById('lb-next');
    var closeBtn = document.getElementById('lb-close');

    images = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));

    document.addEventListener('click', function (e) {
      var target = e.target.closest ? e.target.closest('[data-lightbox]') : null;
      if (target && images.indexOf(target) !== -1) open(images.indexOf(target));
    });

    if (prevBtn) prevBtn.addEventListener('click', function (e) { e.stopPropagation(); step(-1); });
    if (nextBtn) nextBtn.addEventListener('click', function (e) { e.stopPropagation(); step(1); });
    if (closeBtn) closeBtn.addEventListener('click', close);
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) close();
    });
    document.addEventListener('keydown', function (e) {
      if (!isOpen()) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') step(-1);
      else if (e.key === 'ArrowRight') step(1);
    });
  }

  window.Lightbox = { init: init, open: open, close: close };
})();
