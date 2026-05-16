import { Link, useNavigate } from 'react-router-dom';

function Navbar({ user, onLogout }) {
  const navigate = useNavigate();

  function logout() {
    onLogout();
    navigate('/login');
  }

  return (
    <nav style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      height: '52px',
      background: 'var(--surface)',
      borderBottom: '1px solid var(--border)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      <Link to="/" style={{
        fontWeight: 700,
        fontSize: '15px',
        color: 'var(--text)',
        textDecoration: 'none',
        letterSpacing: '-0.01em',
      }}>
        Helpdesk
      </Link>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <span style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
          {user.username}
          <span style={{
            marginLeft: '6px',
            padding: '1px 6px',
            borderRadius: '3px',
            background: 'var(--surface3)',
            border: '1px solid var(--border)',
            fontSize: '11px',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            color: 'var(--text-sub)',
          }}>{user.role}</span>
        </span>

        {user.role === 'user' && (
          <Link to="/tickets/new" style={{ textDecoration: 'none' }}>
            <button className="btn-primary" style={{ padding: '6px 14px', fontSize: '13px' }}>
              + New Ticket
            </button>
          </Link>
        )}

        <button className="btn-secondary" style={{ padding: '6px 12px' }} onClick={logout}>
          Sign out
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
