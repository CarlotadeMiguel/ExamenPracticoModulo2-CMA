const API = 'http://localhost:5000/api/tasks';
const form = document.getElementById('taskForm');
const titleInput = document.getElementById('title');
const prioritySelect = document.getElementById('priority');
const errorDiv = document.getElementById('error');
const list = document.getElementById('taskList');
const filterBtns = document.querySelectorAll('.filter-btn');

let currentFilter = '';

// Carga inicial de tareas
async function fetchTasks() {
  errorDiv.textContent = '';
  try {
    const url = currentFilter ? `${API}?priority=${currentFilter}` : API;
    const res = await fetch(url);
    const tasks = await res.json();
    renderTasks(tasks);
  } catch (e) {
    console.error(e);
    errorDiv.textContent = 'Error al cargar tareas';
  }
}

function renderTasks(tasks) {
  list.innerHTML = '';
  if (!tasks.length) {
    list.innerHTML = '<li>No hay tareas.</li>';
    return;
  }
  tasks.forEach(t => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span>${t.title} [${t.priority}]</span>
      <button class="delete-btn" data-id="${t.id}">Eliminar</button>
    `;
    list.appendChild(li);
  });
}

// Manejo de filtro por prioridad
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    // Resaltar botón activo
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    // Actualizar filtro y recargar tareas
    currentFilter = btn.dataset.filter;
    fetchTasks();
  });
});

// Enviar nueva tarea
form.addEventListener('submit', async e => {
  e.preventDefault();
  errorDiv.textContent = '';
  const title = titleInput.value.trim();
  if (!title) {
    errorDiv.textContent = 'El título es obligatorio';
    return;
  }
  const priority = prioritySelect.value;
  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({title, priority})
    });
    const data = await res.json();
    if (!res.ok) {
      errorDiv.textContent = data.error || 'Error al agregar tarea';
    } else {
      titleInput.value = '';
      fetchTasks();
    }
  } catch (e) {
    console.error(e);
    errorDiv.textContent = 'Error de conexión';
  }
});

// Eliminar tarea
list.addEventListener('click', async e => {
  if (e.target.classList.contains('delete-btn')) {
    const id = e.target.dataset.id;
    try {
      const res = await fetch(`${API}/${id}`, {method:'DELETE'});
      if (!res.ok) {
        const data = await res.json();
        errorDiv.textContent = data.error || 'Error al eliminar tarea';
      } else {
        fetchTasks();
      }
    } catch (e) {
      console.error(e);
      errorDiv.textContent = 'Error de conexión';
    }
  }
});

// Inicializar
fetchTasks();
