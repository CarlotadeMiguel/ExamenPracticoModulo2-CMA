const API = 'http://localhost:5000/api/tasks';
const form = document.getElementById('taskForm');
const titleInput = document.getElementById('title');
const prioritySelect = document.getElementById('priority');
const errorDiv = document.getElementById('error');
const list = document.getElementById('taskList');

// Carga inicial de tareas
async function fetchTasks() {
  try {
    const res = await fetch(API);
    const tasks = await res.json();
    renderTasks(tasks);
  } catch (e) {
    console.error(e);
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
      <button data-id="${t.id}">Eliminar</button>
    `;
    list.appendChild(li);
  });
}

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
    if (!res.ok) {
      const err = await res.json();
      errorDiv.textContent = err.error || 'Error';
    } else {
      titleInput.value = '';
      fetchTasks();
    }
  } catch (e) {
    errorDiv.textContent = 'Error de conexión';
  }
});

// Eliminar tarea
list.addEventListener('click', async e => {
  if (e.target.tagName === 'BUTTON') {
    const id = e.target.dataset.id;
    try {
      await fetch(`${API}/${id}`, {method:'DELETE'});
      fetchTasks();
    } catch (e) {
      console.error(e);
    }
  }
});

// Inicializar
fetchTasks();
