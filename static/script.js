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

/* === Typewriter effect for header logo === */
(function () {
  var cn = "AI 项目作品集";
  var en = "AI Project Portfolio";
  var texts = [cn, en];
  var display = document.getElementById('typingText');
  if (!display) return;

  var textIdx = 0, pos = 0, deleting = false;
  var TYPE_MS = 80, DELETE_MS = 35;
  var PAUSE_AFTER_TYPE = 2000, PAUSE_AFTER_DELETE = 500;

  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  async function step() {
    while (true) {
      var current = texts[textIdx % texts.length];
      if (!deleting) {
        if (pos < current.length) {
          pos++;
          display.textContent = current.slice(0, pos);
          await sleep(TYPE_MS);
        } else {
          await sleep(PAUSE_AFTER_TYPE);
          deleting = true;
        }
      } else {
        if (pos > 0) {
          pos--;
          display.textContent = current.slice(0, pos);
          await sleep(DELETE_MS);
        } else {
          await sleep(PAUSE_AFTER_DELETE);
          deleting = false;
          textIdx++;
        }
      }
    }
  }
  step();
})();

var header = document.querySelector('.header');
var headerInner = document.querySelector('.header .header-inner');
if (header && headerInner) {
  var lastScroll = 0;
  window.addEventListener('scroll', function () {
    var sy = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;

    /* Direction-based dot scaling: scroll up → dots enlarge, scroll down → recover */
    if (sy < 20) {
      header.classList.remove('scroll-up');
    } else if (sy < lastScroll) {
      header.classList.add('scroll-up');
    } else if (sy > lastScroll) {
      header.classList.remove('scroll-up');
    }

    /* Show/hide nav text based on scroll direction */
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
