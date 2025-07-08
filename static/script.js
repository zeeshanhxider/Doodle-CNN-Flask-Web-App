//page navigation
function goToPage(pageId, pushState = true) {
  document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
  const targetPage = document.getElementById(pageId);
  if (targetPage) {
    targetPage.classList.remove('hidden');
    if (pushState) {
      history.pushState({ page: pageId }, '', `#${pageId}`);
    }
    updateNameGif();
  }
}

window.addEventListener('popstate', (event) => {
  const pageId = event.state?.page || location.hash.replace('#', '') || 'welcome-page';
  goToPage(pageId, false);
});

window.addEventListener('DOMContentLoaded', () => {
  const pageId = location.hash.replace('#', '') || 'welcome-page';
  goToPage(pageId, false);
  updateNameGif();
});

//canvas
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas?.getContext('2d');

if (ctx) {
  ctx.imageSmoothingEnabled = true;
  ctx.lineWidth = 35;
  ctx.lineCap = 'round';

  function isDarkMode() {
    return document.body.classList.contains("dark");
  }

  function setCanvasStyles() {
    if (isDarkMode()) {
      ctx.fillStyle = '#1e1e1e';
      ctx.strokeStyle = '#f5f5f5';
    } else {
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = '#000000';
    }
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  setCanvasStyles();

  let drawing = false;
  let lastPos = null;

  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height)
    };
  }

  function startDraw(e) {
    drawing = true;
    lastPos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(lastPos.x, lastPos.y);
  }

  function draw(e) {
    if (!drawing) return;
    const currentPos = getPos(e);
    const midPoint = {
      x: (lastPos.x + currentPos.x) / 2,
      y: (lastPos.y + currentPos.y) / 2
    };

    ctx.quadraticCurveTo(lastPos.x, lastPos.y, midPoint.x, midPoint.y);
    ctx.stroke();
    lastPos = currentPos;
  }

  function stopDraw() {
    drawing = false;
    ctx.beginPath();
    lastPos = null;
  }

  canvas.addEventListener('mousedown', startDraw);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', stopDraw);
  canvas.addEventListener('mouseout', stopDraw);

  canvas.addEventListener('touchstart', startDraw);
  canvas.addEventListener('touchmove', function (e) {
    e.preventDefault();
    draw(e);
  }, { passive: false });
  canvas.addEventListener('touchend', stopDraw);

  document.getElementById("clearBtn").addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setCanvasStyles();
  });

  const toggle = document.getElementById('darkModeToggle');
  toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    setCanvasStyles();
    updateDoodleImageSources();
    updateNameGif();
  });

  function updateDoodleImageSources() {
    const images = document.querySelectorAll('img[src*="/static/assets/doodles"]');
    const mode = isDarkMode() ? "doodles_dark" : "doodles";

    images.forEach(img => {
      const filename = img.src.split("/").pop();
      img.src = `/static/assets/${mode}/${filename}`;
    });
  }
}

//prediction button
document.getElementById('predictBtn').addEventListener('click', () => {
  canvas.toBlob(function (blob) {
    const formData = new FormData();
    formData.append('image', blob, 'canvas.png');

    fetch('/predict', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          alert("Prediction failed: " + data.error);
          return;
        }

        const modal = document.getElementById('predictionModal');
        const modalPrediction = document.getElementById('modalPrediction');
        const closeModal = document.getElementById('closeModal');

        modalPrediction.innerHTML = `Hmm... I think this is <strong>${data.label}</strong> with <strong>${data.confidence}</strong> confidence!`;
        modal.classList.remove('hidden');

        const confettiCanvas = document.createElement('canvas');
        confettiCanvas.classList.add('confetti-canvas');
        document.body.appendChild(confettiCanvas);

        const myConfetti = confetti.create(confettiCanvas, {
          resize: true,
          useWorker: true
        });

        myConfetti({
          particleCount: 150,
          spread: 80,
          startVelocity: 40,
          origin: { x: 0.6, y: 0.5 }
        });

        setTimeout(() => {
          confettiCanvas.remove();
        }, 2000);

        closeModal.onclick = () => modal.classList.add('hidden');
        window.onclick = (e) => {
          if (e.target === modal) modal.classList.add('hidden');
        };
      })
      .catch(err => {
        alert("Error predicting: " + err.message);
      });
  }, 'image/png');
});

//name gif update
function updateNameGif() {
  const nameGif = document.getElementById('nameGif');
  if (nameGif) {
    nameGif.src = isDarkMode() ? '/static/assets/about_elements/name_dark.gif' : '/static/assets/about_elements/name.gif';
  }
}

//candy modal display
setTimeout(() => {
  const candyModal = document.getElementById('candyModal');
  if (candyModal) {
    candyModal.classList.remove('hidden');

    const closeBtn = document.getElementById('closeCandyModal');
    const thankBtn = document.getElementById('thankCandyBtn');

    const closeCandy = () => candyModal.classList.add('hidden');

    closeBtn.addEventListener('click', closeCandy);
    thankBtn.addEventListener('click', closeCandy);

    window.addEventListener('click', (e) => {
      if (e.target === candyModal) closeCandy();
    });
  }
}, 300000);