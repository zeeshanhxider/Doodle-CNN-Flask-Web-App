// handles navigation between pages and updates the browser history
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

// restores page on browser back/forward navigation
window.addEventListener('popstate', (event) => {
  const pageId = event.state?.page || location.hash.replace('#', '') || 'welcome-page';
  goToPage(pageId, false);
});

// loads initial page based on url hash
window.addEventListener('DOMContentLoaded', () => {
  const pageId = location.hash.replace('#', '') || 'welcome-page';
  goToPage(pageId, false);
  updateNameGif();
});

// initialize canvas and context
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas?.getContext('2d');

if (ctx) {
  // sets canvas fill and stroke based on theme
  function setCanvasStyles() {
    if (document.body.classList.contains('dark')) {
      ctx.fillStyle = '#1e1e1e';
      ctx.strokeStyle = '#f5f5f5';
    } else {
      ctx.fillStyle = 'white';
      ctx.strokeStyle = 'black';
    }
    ctx.lineWidth = 15;
    ctx.lineCap = 'round';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  setCanvasStyles();

  let drawing = false;

  // gets cursor or touch position relative to canvas
  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    if (e.touches) {
      return {
        x: (e.touches[0].clientX - rect.left) * (canvas.width / rect.width),
        y: (e.touches[0].clientY - rect.top) * (canvas.height / rect.height)
      };
    } else {
      return {
        x: (e.clientX - rect.left) * (canvas.width / rect.width),
        y: (e.clientY - rect.top) * (canvas.height / rect.height)
      };
    }
  }

  // starts drawing on canvas
  function startDraw(e) {
    drawing = true;
    const pos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
  }

  // draws lines on canvas while mouse/touch is active
  function draw(e) {
    if (!drawing) return;
    const pos = getPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  }

  // stops drawing
  function stopDraw() {
    drawing = false;
    ctx.beginPath();
  }

  // attach mouse and touch drawing events
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

  // clears the canvas on button click
  document.getElementById("clearBtn").addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = isDarkMode() ? "#1e1e1e" : "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  });

  // checks if dark mode is active
  function isDarkMode() {
    return document.body.classList.contains("dark");
  }

  // handles prediction logic and shows modal with result
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

          // triggers confetti effect
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
            origin: {
              x: 0.58,
              y: 0.5
            }
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

  // toggles dark mode and updates ui accordingly
  const toggle = document.getElementById('darkModeToggle');
  const circle = toggle.querySelector('.circle');

  toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    setCanvasStyles();
    updateDoodleImageSources();
    updateNameGif();
  });

  // updates doodle image paths based on theme
  function updateDoodleImageSources() {
    const images = document.querySelectorAll('img[src*="/static/assets/doodles"]');
    const mode = isDarkMode() ? "doodles_dark" : "doodles";

    images.forEach(img => {
      const filename = img.src.split("/").pop();
      img.src = `/static/assets/${mode}/${filename}`;
    });
  }
}

// updates the gif under the name based on theme
function updateNameGif() {
  const nameGif = document.getElementById('nameGif');
  if (nameGif) {
    nameGif.src = isDarkMode() ? '/static/assets/about_elements/name_dark.gif' : '/static/assets/about_elements/name.gif';
  }
}

// shows candy modal after delay and handles closing
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