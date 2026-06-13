function copyCode(btn) {
  var pre = btn.closest('.project-code').querySelector('pre');
  var code = pre.textContent;
  navigator.clipboard.writeText(code).then(function () {
    btn.textContent = '已复制';
    btn.classList.add('copied');
    setTimeout(function () {
      btn.textContent = '复制';
      btn.classList.remove('copied');
    }, 2000);
  }).catch(function () {
    var ta = document.createElement('textarea');
    ta.value = code; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    document.execCommand('copy'); document.body.removeChild(ta);
    btn.textContent = '已复制'; btn.classList.add('copied');
    setTimeout(function () {
      btn.textContent = '复制'; btn.classList.remove('copied');
    }, 2000);
  });
}

function openLightbox(img) {
  var lb = document.getElementById('lightbox');
  if (!lb) {
    lb = document.createElement('div');
    lb.id = 'lightbox'; lb.className = 'lightbox';
    lb.onclick = function () { lb.classList.remove('active'); };
    var lbImg = document.createElement('img');
    lbImg.id = 'lightbox-img';
    lb.appendChild(lbImg);
    document.body.appendChild(lb);
  }
  document.getElementById('lightbox-img').src = img.src;
  lb.classList.add('active');
}

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    var lb = document.getElementById('lightbox');
    if (lb) lb.classList.remove('active');
  }
});

var headerInner = document.querySelector('.header .header-inner');
if (headerInner) {
  var lastScroll = 0;
  window.addEventListener('scroll', function () {
    var sy = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
    if (sy < 50) {
      headerInner.style.opacity = '1';
    } else if (sy > lastScroll) {
      headerInner.style.opacity = '0';
    } else if (sy < lastScroll) {
      headerInner.style.opacity = '1';
    }
    lastScroll = sy;
  });
}
