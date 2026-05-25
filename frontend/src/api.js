const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function getToken() {
  return localStorage.getItem('token');
}

function authHeaders() {
  return { Authorization: `Bearer ${getToken()}` };
}

export async function register(username, email, password) {
  const res = await fetch(`${BASE}/api/v1/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ username, email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Registration failed');
  }
  return res.json();
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);

  const res = await fetch(
    `${BASE}/api/v1/auth/login`,
    { 
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      credentials: 'include',
      body: form
    }
  );
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Login failed');
  }
  return res.json();
}

export async function getTickets(status, priority) {
  const params = new URLSearchParams();
  if (status) params.append('status', status);
  if (priority) params.append('priority', priority);
  const res = await fetch(`${BASE}/api/v1/tickets/?${params}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error('Failed to fetch tickets');
  return res.json();
}

export async function getTicket(id) {
  const res = await fetch(`${BASE}/api/v1/tickets/${id}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error('Failed to fetch ticket');
  return res.json();
}

export async function createTicket(title, description, priority, file) {
  const form = new FormData();
  form.append('title', title);
  form.append('description', description);
  form.append('priority', priority);
  if (file) form.append('file', file);

  const res = await fetch(`${BASE}/api/v1/tickets/`, {
    method: 'POST',
    headers: authHeaders(),
    body: form,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to create ticket');
  }
  return res.json();
}

export async function getSupportUsers() {
  const res = await fetch(`${BASE}/api/v1/users/support`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error('Failed to fetch support users');
  return res.json();
}

export async function assignTicket(ticketId, supportUserId) {
  const res = await fetch(`${BASE}/api/v1/tickets/${ticketId}/assign`, {
    method: 'PATCH',
    headers: {
      ...authHeaders(),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ support_user_id: supportUserId }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to assign ticket');
  }
  return res.json();
}

export async function updateTicket(ticketId, updateData) {
  const res = await fetch(`${BASE}/api/v1/tickets/${ticketId}`, {
    method: 'PATCH',
    headers: {
      ...authHeaders(),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updateData),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to update ticket');
  }
  return res.json();
}
