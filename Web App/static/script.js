function goToPage(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
  document.getElementById(pageId).classList.remove('hidden');
}

const canvas = document.getElementById('drawingCanvas');
const ctx = canvas?.getContext('2d');

if (ctx) {
  function setCanvasStyles() {
    if (document.body.classList.contains('dark')) {
      ctx.fillStyle = '#1e1e1e';
      ctx.strokeStyle = '#f5f5f5';
    } else {
      ctx.fillStyle = 'white';
      ctx.strokeStyle = 'black';
    }
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  setCanvasStyles();

  let drawing = false;

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

  function startDraw(e) {
    drawing = true;
    const pos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
  }

  function draw(e) {
    if (!drawing) return;
    const pos = getPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  }

  function stopDraw() {
    drawing = false;
    ctx.beginPath();
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
  ctx.fillStyle = isDarkMode() ? "#1e1e1e" : "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
});

function isDarkMode() {
  return document.body.classList.contains("dark");
}

  document.getElementById('downloadBtn').addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = 'drawing.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  });

  const toggle = document.getElementById('darkModeToggle');
  const circle = toggle.querySelector('.circle');

  toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');

    setCanvasStyles();
  });
}