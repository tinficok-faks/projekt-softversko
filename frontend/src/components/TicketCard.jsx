import { Link } from 'react-router-dom';

function TicketCard({ ticket, userRole }) {
  const date = new Date(ticket.created_at).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
  });

  return (
    <Link to={`/tickets/${ticket.id}`} style={{ textDecoration: 'none', display: 'block', marginBottom: '8px' }}>
      <div
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius)',
          padding: '16px 20px',
          cursor: 'pointer',
          transition: 'border-color 0.15s, background 0.15s',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '16px',
        }}
        onMouseEnter={e => {
          e.currentTarget.style.borderColor = 'var(--border-light)';
          e.currentTarget.style.background = 'var(--surface2)';
        }}
        onMouseLeave={e => {
          e.currentTarget.style.borderColor = 'var(--border)';
          e.currentTarget.style.background = 'var(--surface)';
        }}
      >
        <div style={{ minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <p style={{ fontWeight: 600, fontSize: '14px', color: 'var(--text)', margin: 0 }}>
              {ticket.title}
            </p>
            {(userRole === 'admin' || userRole === 'support') && ticket.created_by_user && (
              <span style={{ fontSize: '12px', color: 'var(--text-sub)', background: 'var(--surface2)', padding: '2px 6px', borderRadius: '4px' }}>
                by @{ticket.created_by_user.username}
              </span>
            )}
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {ticket.description.length > 100 ? ticket.description.slice(0, 100) + '…' : ticket.description}
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
          <span className={`badge badge-${ticket.priority}`}>{ticket.priority}</span>
          <span className={`badge badge-${ticket.status}`}>{ticket.status.replace('_', ' ')}</span>
          <span style={{ color: 'var(--text-muted)', fontSize: '12px', marginLeft: '8px' }}>{date}</span>
        </div>
      </div>
    </Link>
  );
}

export default TicketCard;
