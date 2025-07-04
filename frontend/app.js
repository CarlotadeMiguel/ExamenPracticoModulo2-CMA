const API = 'http://localhost:5000/api/tasks';
const form = document.getElementById('taskForm');
const titleInput = document.getElementById('title');
const prioritySelect = document.getElementById('priority');
const errorDiv = document.getElementById('error');
const list = document.getElementById('taskList');
const filterBtns = document.querySelectorAll('.filter-btn');

let currentFilter = '';

// -------- Inicializar y cargar tareas --------
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

// -------- Render de tareas (list + botones) --------
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
      <button class="edit-btn" data-id="${t.id}">✏️</button>
      <button class="delete-btn" data-id="${t.id}">🗑️</button>
    `;
    list.appendChild(li);
  });
}

// -------- Filtros --------
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    fetchTasks();
  });
});

// -------- Añadir nueva tarea --------
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
  } catch {
    showError('Error de conexión');
  }
});

// -------- Eliminar, Iniciar Edición, Guardar y Cancelar --------
list.addEventListener('click', async e => {
  const li = e.target.closest('li');
  const id = e.target.dataset.id;

  // Eliminar
  if (e.target.classList.contains('delete-btn')) {
    clearError();
    try {
      const res = await fetch(`${API}/${id}`, { method: 'DELETE' });
      const data = await res.json();
      if (!res.ok) showError(data.error || 'Error al eliminar tarea');
      else fetchTasks();
    } catch {
      showError('Error de conexión');
    }
    return;
  }

  // Iniciar edición
  if (e.target.classList.contains('edit-btn')) {
    clearError();
    const span = li.querySelector('span');
    const [titleText, priorityText] = span.textContent.split(' [');
    const currentPriority = priorityText.replace(']', '');
    li.innerHTML = `
      <input class="edit-title" value="${titleText.trim()}" />
      <select class="edit-priority">
        <option value="baja"${currentPriority==='baja'?' selected':''}>Baja</option>
        <option value="media"${currentPriority==='media'?' selected':''}>Media</option>
        <option value="alta"${currentPriority==='alta'?' selected':''}>Alta</option>
      </select>
      <button class="save-btn" data-id="${id}">Guardar</button>
      <button class="cancel-btn">✖️</button>
    `;
    return;
  }

  // Guardar edición
  if (e.target.classList.contains('save-btn')) {
    clearError();
    const title = li.querySelector('.edit-title').value.trim();
    const priority = li.querySelector('.edit-priority').value;
    if (!title) {
      showError('El título es obligatorio');
      return;
    }
    try {
      const res = await fetch(`${API}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, priority })
      });
      const data = await res.json();
      if (!res.ok) handleErrors(data);
      else fetchTasks();
    } catch {
      showError('Error de conexión');
    }
    return;
  }

  // Cancelar edición
  if (e.target.classList.contains('cancel-btn')) {
    fetchTasks();
    return;
  }
});

// -------- Manejo de errores --------
function handleErrors(data) {
  if (data.errors) {
    const msgs = Object.values(data.errors).flat();
    showError(msgs.join(' • '));
  } else if (data.error) {
    showError(data.error);
  } else {
    showError('Error desconocido');
  }
}

function showError(msg) {
  errorDiv.innerHTML = `<div class="error-message">${msg}</div>`;
}

function clearError() {
  errorDiv.textContent = '';
}

// Limpiar error al editar campos
titleInput.addEventListener('input', clearError);
prioritySelect.addEventListener('change', clearError);

// -------- Ejecutar --------
fetchTasks();
