const $ = (id) => document.getElementById(id);

function showDate() {
  $("today").textContent = new Date().toLocaleDateString(undefined, {
    weekday: "short", month: "short", day: "numeric", year: "numeric"
  });
}

async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}

function renderTasks(tasks) {
  const list = $("task-list");
  $("task-total").textContent = `${tasks.length} tasks`;
  if (!tasks.length) {
    list.innerHTML = '<p class="muted">No tasks yet. Add your first task above.</p>';
    return;
  }
  list.innerHTML = tasks.map(task => `
    <div class="task-item">
      <div><strong>${escapeHtml(task.title)}</strong><small>Due: ${escapeHtml(task.due_date)}</small></div>
      <select aria-label="Status for ${escapeHtml(task.title)}" data-task-id="${task.id}">
        ${["Pending", "In progress", "Completed"].map(status =>
          `<option ${task.status === status ? "selected" : ""}>${status}</option>`
        ).join("")}
      </select>
    </div>`).join("");
  list.querySelectorAll("select").forEach(select => {
    select.addEventListener("change", async (event) => {
      try {
        await api(`/api/tasks/${event.target.dataset.taskId}`, {
          method: "PATCH",
          body: JSON.stringify({ status: event.target.value })
        });
        await loadDashboard();
      } catch (error) {
        $("task-feedback").textContent = error.message;
      }
    });
  });
}

function renderAnnouncements(items) {
  $("announcement-list").innerHTML = items.length ? items.map(item => `
    <div class="announcement">
      <h4>${escapeHtml(item.title)}</h4>
      <p>${escapeHtml(item.message)}</p>
      <small>Posted ${escapeHtml(item.posted_on)}</small>
    </div>`).join("") : '<p class="muted">No announcements available.</p>';
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[char]));
}

async function loadDashboard() {
  try {
    const data = await api("/api/dashboard");
    $("attendance").textContent = `${data.student.attendance}%`;
    $("attendance-bar").style.width = `${data.student.attendance}%`;
    $("cgpa").textContent = data.student.cgpa.toFixed(2);
    $("pending-count").textContent = data.stats.pending_tasks;
    $("completed-count").textContent = data.stats.completed_tasks;
    $("student-name").textContent = data.student.name;
    $("student-course").textContent = `${data.student.department} · ${data.student.year}`;
    $("register-number").textContent = data.student.register_number;
    renderTasks(data.tasks);
    renderAnnouncements(data.announcements);
  } catch (error) {
    $("task-list").innerHTML = `<p class="muted">${escapeHtml(error.message)} Check that the Python server is running.</p>`;
  }
}

$("task-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  $("task-feedback").textContent = "";
  try {
    await api("/api/tasks", {
      method: "POST",
      body: JSON.stringify({
        title: $("task-title").value.trim(),
        due_date: $("task-date").value
      })
    });
    $("task-title").value = "";
    $("task-date").value = "";
    await loadDashboard();
  } catch (error) {
    $("task-feedback").textContent = error.message;
  }
});

showDate();
loadDashboard();
