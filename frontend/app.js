let participantes = [];

async function cargarParticipantes() {
  const url = document.getElementById('postUrl').value.trim();
  if (!url) return alert('Por favor ingresá un enlace válido de Instagram.');

  const btn = document.getElementById('btnCargar');
  btn.innerText = '⌛ OBTENIENDO TODOS LOS COMENTARIOS...';
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
    } else {
      alert(data.detail || 'No se pudieron obtener los comentarios.');
    }
  } catch (err) {
    alert('Error de conexión con el servidor.');
  } finally {
    btn.innerText = '🎸 CARGAR PARTICIPANTES';
    btn.disabled = false;
  }
}

function abrirModalSorteo() {
  if (participantes.length === 0) return;
  document.getElementById('modalSorteo').classList.remove('hidden');
  iniciarSorteoAnimado();
}

function cerrarModalSorteo() {
  document.getElementById('modalSorteo').classList.add('hidden');
}

function iniciarSorteoAnimado() {
  const ruletaBox = document.getElementById('ruletaBox');
  const ruletaNombre = document.getElementById('ruletaNombre');
  const ganadorBox = document.getElementById('ganadorBox');
  const nombreGanador = document.getElementById('nombreGanador');
  const fotoGanador = document.getElementById('fotoGanador');
  const btnReintentar = document.getElementById('btnReintentar');

  ruletaBox.classList.remove('hidden');
  ganadorBox.classList.add('hidden');
  btnReintentar.classList.add('hidden');

  let giros = 0;
  const totalGiros = 35; // ~3.5 segundos girando

  const intervalo = setInterval(() => {
    const pAleatorio = participantes[Math.floor(Math.random() * participantes.length)];
    ruletaNombre.innerText = `@${pAleatorio.username}`;
    giros++;

    if (giros >= totalGiros) {
      clearInterval(intervalo);
      
      const ganadorFinal = participantes[Math.floor(Math.random() * participantes.length)];
      
      ruletaBox.classList.add('hidden');
      nombreGanador.innerText = `@${ganadorFinal.username}`;
      
      fotoGanador.src = (ganadorFinal.profile_pic && ganadorFinal.profile_pic !== "")
        ? ganadorFinal.profile_pic 
        : 'assets/logo-totos.png';

      ganadorBox.classList.remove('hidden');
      btnReintentar.classList.remove('hidden');

      if (typeof confetti === 'function') {
        confetti({ particleCount: 150, spread: 80, origin: { y: 0.5 } });
      }
    }
  }, 100);
}