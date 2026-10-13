let participantes = [];

async function cargarParticipantes() {
  const url = document.getElementById('postUrl').value.trim();
  if (!url) return alert('Por favor ingresá un enlace válido de Instagram.');

  const btn = document.getElementById('btnCargar');
  btn.innerText = '⌛ CARGANDO COMENTARIOS...';
  btn.disabled = true;

  try {
    const response = await fetch('https://sorteos-totos-rock.onrender.com/api/obtener-participantes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ post_url: url })
    });

    const data = await response.json();

    if (data.exito) {
      participantes = data.participantes;
      document.getElementById('totalCount').innerText = data.total_unicos;
      document.getElementById('resultadoSection').classList.remove('hidden');
      document.getElementById('ganadorBox').classList.add('hidden');
      document.getElementById('ruletaBox').classList.add('hidden');
    } else {
      alert(data.detail || 'No se pudieron obtener los comentarios.');
    }
  } catch (err) {
    alert('Error de conexión con el servidor. Por favor intentá de nuevo.');
  } finally {
    btn.innerText = '🎸 CARGAR PARTICIPANTES';
    btn.disabled = false;
  }
}

function realizarSorteo() {
  if (participantes.length === 0) return;

  const btnSortear = document.getElementById('btnSortear');
  const ruletaBox = document.getElementById('ruletaBox');
  const ruletaNombre = document.getElementById('ruletaNombre');
  const ganadorBox = document.getElementById('ganadorBox');
  const nombreGanador = document.getElementById('nombreGanador');

  btnSortear.disabled = true;
  ganadorBox.classList.add('hidden');
  ruletaBox.classList.remove('hidden');

  let giros = 0;
  const totalGiros = 30; // Duración del giro de la ruleta

  const intervalo = setInterval(() => {
    const indiceAleatorio = Math.floor(Math.random() * participantes.length);
    ruletaNombre.innerText = `@${participantes[indiceAleatorio]}`;
    giros++;

    if (giros >= totalGiros) {
      clearInterval(intervalo);
      
      // Ganador definitivo
      const ganadorFinal = participantes[Math.floor(Math.random() * participantes.length)];
      
      ruletaBox.classList.add('hidden');
      nombreGanador.innerText = `@${ganadorFinal}`;
      ganadorBox.classList.remove('hidden');
      btnSortear.disabled = false;

      // Disparar confeti
      if (typeof confetti === 'function') {
        confetti({
          particleCount: 120,
          spread: 70,
          origin: { y: 0.6 }
        });
      }
    }
  }, 100);
}