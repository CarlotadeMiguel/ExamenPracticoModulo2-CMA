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
  clearError();
  try {
    const url = currentFilter ? `${API}?priority=${currentFilter}` : API;
    const res = await fetch(url);
    const tasks = await res.json();
    renderTasks(tasks);
  } catch (e) {
    console.error(e);
    showError('Error al cargar tareas');
  }
}

// Renderiza la lista de tareas
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
      <button class="delete-btn" data-id="${t.id}">🗑️</button>
    `;
    list.appendChild(li);
  });
}

// Filtros por prioridad
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    fetchTasks();
  });
});

// Validación y envío de nueva tarea
form.addEventListener('submit', async e => {
  e.preventDefault();
  clearError();
  const title = titleInput.value.trim();
  if (!title) {
    showError('El título es obligatorio');
    return;
  }
  const priority = prioritySelect.value;

  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, priority })
    });
    const data = await res.json();
    if (!res.ok) {
      handleErrors(data);
    } else {
      titleInput.value = '';
      fetchTasks();
    }
  } catch (e) {
    console.error(e);
    showError('Error de conexión');
  }
});

// Eliminar tarea
list.addEventListener('click', async e => {
  if (!e.target.classList.contains('delete-btn')) return;
  clearError();
  const id = e.target.dataset.id;
  try {
    const res = await fetch(`${API}/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (!res.ok) {
      showError(data.error || 'Error al eliminar tarea');
    } else {
      fetchTasks();
    }
  } catch (e) {
    console.error(e);
    showError('Error de conexión');
  }
});

// Procesa errores del backend (Marshmallow)
function handleErrors(data) {
  if (data.errors) {
    // Unir todos los mensajes de los campos
    const msgs = Object.values(data.errors).flat();
    showError(msgs.join(' • '));
  } else if (data.error) {
    showError(data.error);
  } else {
    showError('Error desconocido');
  }
}

// Muestra un mensaje de error bajo el formulario
function showError(msg) {
  errorDiv.innerHTML = `<div class="error-message">${msg}</div>`;
}

// Limpia el contenedor de errores
function clearError() {
  errorDiv.textContent = '';
}

// Limpiar error al modificar campos
titleInput.addEventListener('input', clearError);
prioritySelect.addEventListener('change', clearError);

// Inicializar
fetchTasks();
