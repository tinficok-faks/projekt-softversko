import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTicket, getSupportUsers, assignTicket, updateTicket } from '../api';

function TicketDetail({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [supportUsers, setSupportUsers] = useState([]);
  const [selectedSupport, setSelectedSupport] = useState('');
  const [assigning, setAssigning] = useState(false);

  useEffect(() => {
    getTicket(id)
      .then(setTicket)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));

    if (user.role === 'admin') {
      getSupportUsers()
        .then(setSupportUsers)
        .catch(console.error);
    }
  }, [id, user.role]);

  async function handleAssign() {
    if (!selectedSupport) return;
    setAssigning(true);
    try {
      const updatedTicket = await assignTicket(id, selectedSupport);
      setTicket(updatedTicket);
    } catch (err) {
      alert(err.message);
    } finally {
      setAssigning(false);
    }
  }

  async function handleStatusUpdate(newStatus) {
    try {
      const updatedTicket = await updateTicket(id, { status: newStatus });
      setTicket(updatedTicket);
    } catch (err) {
      alert(err.message);
    }
  }

  function fmt(dt) {
    return new Date(dt).toLocaleString('en-GB', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  }

  if (loading) return <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '80px 0' }}>Loading ticket…</p>;
  if (error) return <p className="error" style={{ padding: '40px 24px', textAlign: 'center' }}>{error}</p>;
  if (!ticket) return null;

  return (
    <div style={{ maxWidth: '720px', margin: '0 auto', padding: '40px 24px' }}>
      <button
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          color: 'var(--text-muted)',
          fontSize: '13px',
          marginBottom: '24px',
          cursor: 'pointer',
          background: 'none',
          border: 'none',
          padding: 0,
        }}
        onClick={() => navigate('/')}
      >
        ← Back to tickets
      </button>

      <div style={{
        background: 'var(--surface)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius)',
        padding: '32px',
      }}>
        <h1 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '24px', color: 'var(--text)', lineHeight: 1.3 }}>
          {ticket.title}
        </h1>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: '16px',
          marginBottom: '28px',
          paddingBottom: '24px',
          borderBottom: '1px solid var(--border-light)',
        }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <span style={{ color: 'var(--text-sub)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>Status</span>
            <span className={`badge badge-${ticket.status}`} style={{ alignSelf: 'flex-start' }}>{ticket.status.replace('_', ' ')}</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <span style={{ color: 'var(--text-sub)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>Priority</span>
            <span className={`badge badge-${ticket.priority}`} style={{ alignSelf: 'flex-start' }}>{ticket.priority}</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <span style={{ color: 'var(--text-sub)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>Created by</span>
            <span style={{ fontWeight: 500, fontSize: '13px', color: 'var(--text)' }}>
              {ticket.created_by_user ? ticket.created_by_user.username : ticket.created_by_id}
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <span style={{ color: 'var(--text-sub)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>Created</span>
            <span style={{ fontWeight: 500, fontSize: '13px' }}>{fmt(ticket.created_at)}</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <span style={{ color: 'var(--text-sub)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>Last updated</span>
            <span style={{ fontWeight: 500, fontSize: '13px' }}>{fmt(ticket.updated_at)}</span>
          </div>
          {ticket.assigned_to_id && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ color: 'var(--text-sub)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>Assigned to</span>
              <span style={{ fontWeight: 500, fontSize: '13px', color: 'var(--text)' }}>{ticket.assigned_to_id}</span>
            </div>
          )}
        </div>

        <div style={{ lineHeight: 1.7, color: 'var(--text)', whiteSpace: 'pre-wrap', fontSize: '14px' }}>
          {ticket.description}
        </div>

        {ticket.attachments && ticket.attachments.length > 0 && (
          <div style={{ marginTop: '32px', paddingTop: '24px', borderTop: '1px solid var(--border-light)' }}>
            <h3 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-sub)', marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Attachments
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {ticket.attachments.map(att => (
                <a
                  key={att.id}
                  href={`http://localhost:8000/${att.file_path}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '12px 16px',
                    background: 'var(--bg)',
                    border: '1px solid var(--border)',
                    borderRadius: 'var(--radius)',
                    textDecoration: 'none',
                    color: 'var(--text)',
                    fontSize: '14px',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--primary)'}
                  onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
                >
                  <span style={{ fontSize: '18px' }}>📎</span>
                  <span style={{ textDecoration: 'underline' }}>{att.file_name}</span>
                </a>
              ))}
            </div>
          </div>
        )}

        {(user.role === 'admin' || user.role === 'support') && (
          <div style={{ marginTop: '40px', paddingTop: '24px', borderTop: '1px solid var(--border-light)' }}>
            <h3 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-sub)', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Actions
            </h3>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center', flexWrap: 'wrap' }}>
              {ticket.status !== 'resolved' && (
                <button
                  className="btn-secondary"
                  onClick={() => handleStatusUpdate('resolved')}
                >
                  Mark as Solved
                </button>
              )}
              {ticket.status !== 'closed' && (
                <button
                  className="btn-secondary"
                  onClick={() => handleStatusUpdate('closed')}
                >
                  Close Ticket
                </button>
              )}
              {ticket.status !== 'in_progress' && (
                <button
                  className="btn-secondary"
                  onClick={() => handleStatusUpdate('in_progress')}
                >
                  Mark In Progress
                </button>
              )}
            </div>
          </div>
        )}

        {user.role === 'admin' && (
          <div style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid var(--border-light)' }}>
            <h3 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-sub)', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              {ticket.assigned_to_id ? 'Reassign Ticket' : 'Assign Ticket'}
            </h3>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <select
                value={selectedSupport}
                onChange={e => setSelectedSupport(e.target.value)}
                style={{ maxWidth: '240px' }}
              >
                <option value="">Select support user...</option>
                {supportUsers.map(su => (
                  <option key={su.id} value={su.id}>{su.username}</option>
                ))}
              </select>
              <button
                className="btn-primary"
                onClick={handleAssign}
                disabled={!selectedSupport || assigning}
              >
                {assigning ? 'Assigning...' : (ticket.assigned_to_id ? 'Reassign' : 'Assign')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default TicketDetail;
