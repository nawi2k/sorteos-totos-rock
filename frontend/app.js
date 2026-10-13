let participantes = [];

async function cargarParticipantes() {
  const url = document.getElementById('postUrl').value.trim();
  if (!url) return alert('Por favor ingresá un enlace válido de Instagram.');

  const btn = document.getElementById('btnCargar');
  btn.innerText = '⌛ OBTENIENDO COMENTARIOS...';
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

function abrirSorteoModal() {
  if (participantes.length === 0) return;
  document.getElementById('sorteoModal').classList.remove('hidden');
  iniciarAnimacionSorteo();
}

function cerrarSorteoModal() {
  document.getElementById('sorteoModal').classList.add('hidden');
}

function iniciarAnimacionSorteo() {
  const ruletaBox = document.getElementById('ruletaBox');
  const ruletaNombre = document.getElementById('ruletaNombre');
  const ganadorBox = document.getElementById('ganadorBox');
  const nombreGanador = document.getElementById('nombreGanador');
  const fotoGanador = document.getElementById('fotoGanador');
  const btnRepetir = document.getElementById('btnRepetir');

  ruletaBox.classList.remove('hidden');
  ganadorBox.classList.add('hidden');
  btnRepetir.classList.add('hidden');

  let giros = 0;
  const totalGiros = 35; // Tiempo de ruleta (~3.5 seg)

  const intervalo = setInterval(() => {
    const pAleatorio = participantes[Math.floor(Math.random() * participantes.length)];
    ruletaNombre.innerText = `@${pAleatorio.username}`;
    giros++;

    if (giros >= totalGiros) {
      clearInterval(intervalo);
      
      const ganadorFinal = participantes[Math.floor(Math.random() * participantes.length)];
      
      ruletaBox.classList.add('hidden');
      nombreGanador.innerText = `@${ganadorFinal.username}`;
      
      // Manejo de la foto de perfil
      fotoGanador.src = (ganadorFinal.profile_pic && ganadorFinal.profile_pic !== '') 
        ? ganadorFinal.profile_pic 
        : 'assets/logo-totos.png';
      
      ganadorBox.classList.remove('hidden');
      btnRepetir.classList.remove('hidden');

      if (typeof confetti === 'function') {
        confetti({ particleCount: 150, spread: 80, origin: { y: 0.5 } });
      }
    }
  }, 100);
}