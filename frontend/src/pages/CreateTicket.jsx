import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createTicket } from '../api';

function CreateTicket() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    if (!title.trim() || !description.trim()) {
      setError('Title and description are required.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const ticket = await createTicket(title, description, priority, file);
      navigate(`/tickets/${ticket.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: '620px', margin: '0 auto', padding: '40px 24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '6px' }}>Open a New Ticket</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
          Please provide details about the issue you're facing.
        </p>
      </div>
      
      <div style={{ borderTop: '1px solid var(--border)', marginBottom: '24px' }} />

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', fontWeight: 500, color: 'var(--text-sub)' }}>
            Title
          </label>
          <input
            id="ticket-title"
            type="text"
            placeholder="Brief description of the issue"
            value={title}
            onChange={e => setTitle(e.target.value)}
            autoFocus
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', fontWeight: 500, color: 'var(--text-sub)' }}>
            Description
          </label>
          <textarea
            id="ticket-description"
            placeholder="Provide as much detail as possible…"
            rows={6}
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', fontWeight: 500, color: 'var(--text-sub)' }}>
            Priority
          </label>
          <select
            id="ticket-priority"
            value={priority}
            onChange={e => setPriority(e.target.value)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '6px', fontSize: '13px', fontWeight: 500, color: 'var(--text-sub)' }}>
            Attachment (optional)
          </label>
          <input
            id="ticket-file"
            type="file"
            style={{ 
              padding: '8px 12px', 
              background: 'var(--surface2)', 
              border: '1px solid var(--border)',
              color: 'var(--text-muted)'
            }}
            onChange={e => setFile(e.target.files[0] || null)}
          />
        </div>

        {error && <p className="error">{error}</p>}

        <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
          <button
            id="create-submit"
            className="btn-primary"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Submitting…' : 'Submit Ticket'}
          </button>
          <button
            className="btn-secondary"
            type="button"
            onClick={() => navigate('/')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreateTicket;
