let participantes = [];

function cambiarTab(tipo) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));

  if (tipo === 'link') {
    event.target.classList.add('active');
    document.getElementById('tabLink').classList.remove('hidden');
  } else {
    event.target.classList.add('active');
    document.getElementById('tabManual').classList.remove('hidden');
  }
}

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
      mostrarSeccionResultados();
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

function procesarManual() {
  const texto = document.getElementById('textoManual').value;
  if (!texto.trim()) return alert('Por favor pegá algún texto o lista de usuarios.');

  // Extraer nombres de usuario usando Expresión Regular
  const coincidencias = texto.match(/@?([a-zA-Z0-9_.-]+)/g) || [];
  const setUnicos = new Set();

  coincidencias.forEach(u => {
    let limpio = u.replace('@', '').trim().toLowerCase();
    if (limpio.length > 2) setUnicos.add(limpio);
  });

  if (setUnicos.size === 0) return alert('No se detectaron usuarios válidos.');

  participantes = Array.from(setUnicos).sort();
  mostrarSeccionResultados();
}

function mostrarSeccionResultados() {
  document.getElementById('totalCount').innerText = participantes.length;
  document.getElementById('resultadoSection').classList.remove('hidden');
  document.getElementById('ganadorBox').classList.add('hidden');
  document.getElementById('ruletaBox').classList.add('hidden');
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
  const totalGiros = 30;

  const intervalo = setInterval(() => {
    const indiceAleatorio = Math.floor(Math.random() * participantes.length);
    ruletaNombre.innerText = `@${participantes[indiceAleatorio]}`;
    giros++;

    if (giros >= totalGiros) {
      clearInterval(intervalo);
      const ganadorFinal = participantes[Math.floor(Math.random() * participantes.length)];
      
      ruletaBox.classList.add('hidden');
      nombreGanador.innerText = `@${ganadorFinal}`;
      ganadorBox.classList.remove('hidden');
      btnSortear.disabled = false;

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