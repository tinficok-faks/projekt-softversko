import { useState, useEffect } from 'react';
import { getTickets } from '../api';
import TicketCard from '../components/TicketCard';

const STATUSES = ['new', 'in_progress', 'resolved', 'closed'];
const PRIORITIES = ['low', 'medium', 'high'];

function Dashboard({ user }) {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');

  const isAdmin = user.role === 'admin';

  useEffect(() => {
    setLoading(true);
    setError('');
    getTickets(statusFilter || undefined, priorityFilter || undefined)
      .then(setTickets)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [statusFilter, priorityFilter]);

  function heading() {
    if (user.role === 'admin') return 'All Tickets';
    if (user.role === 'support') return 'Assigned to Me';
    return 'My Tickets';
  }

  return (
    <div style={{ maxWidth: '860px', margin: '0 auto', padding: '40px 24px' }}>

      {/* Header row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '18px', fontWeight: 700 }}>{heading()}</h1>
          {!loading && (
            <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '2px' }}>
              {tickets.length} ticket{tickets.length !== 1 ? 's' : ''}
            </p>
          )}
        </div>

        {isAdmin && (
          <div style={{ display: 'flex', gap: '8px' }}>
            <select
              id="filter-status"
              style={{ width: 'auto', minWidth: '140px' }}
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
            >
              <option value="">All statuses</option>
              {STATUSES.map(s => (
                <option key={s} value={s}>{s.replace('_', ' ')}</option>
              ))}
            </select>
            <select
              id="filter-priority"
              style={{ width: 'auto', minWidth: '130px' }}
              value={priorityFilter}
              onChange={e => setPriorityFilter(e.target.value)}
            >
              <option value="">All priorities</option>
              {PRIORITIES.map(p => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Divider */}
      <div style={{ borderTop: '1px solid var(--border)', marginBottom: '20px' }} />

      {loading && (
        <p style={{ color: 'var(--text-muted)', fontSize: '13px', padding: '40px 0', textAlign: 'center' }}>
          Loading…
        </p>
      )}
      {error && <p className="error">{error}</p>}
      {!loading && !error && tickets.length === 0 && (
        <p style={{ color: 'var(--text-muted)', fontSize: '13px', padding: '40px 0', textAlign: 'center' }}>
          No tickets found.
        </p>
      )}
      {!loading && tickets.map(ticket => (
        <TicketCard key={ticket.id} ticket={ticket} userRole={user.role} />
      ))}
    </div>
  );
}

export default Dashboard;
