let participantes = [];

async function cargarParticipantes() {
  const url = document.getElementById('postUrl').value;
  if (!url) return alert('Por favor ingresá un enlace válido.');

  const btn = document.getElementById('btnCargar');
  btn.innerText = 'Cargando comentarios...';
  btn.disabled = true;

  try {
    // Reemplazar URL con la del servidor desplegado
    const response = await fetch('http://localhost:8000/api/obtener-participantes', {
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
      alert('No se pudieron obtener los comentarios.');
    }
  } catch (err) {
    alert('Error de conexión con el servidor.');
  } finally {
    btn.innerText = 'Cargar Participantes';
    btn.disabled = false;
  }
}

function realizarSorteo() {
  if (participantes.length === 0) return;

  const ganadorBox = document.getElementById('ganadorBox');
  const nombreGanador = document.getElementById('nombreGanador');

  const indice = Math.floor(Math.random() * participantes.length);
  const ganador = participantes[indice];

  nombreGanador.innerText = `@${ganador}`;
  ganadorBox.classList.remove('hidden');
}