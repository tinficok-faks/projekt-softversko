import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { login } from '../api';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    if (!username || !password) { setError('All fields are required.'); return; }
    setError('');
    setLoading(true);
    try {
      const data = await login(username, password);
      onLogin(data);
      navigate('/');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '24px',
    }}>
      <div style={{ width: '100%', maxWidth: '380px' }}>
        <div style={{ marginBottom: '32px' }}>
          <h1 style={{ fontSize: '22px', fontWeight: 700, marginBottom: '6px' }}>Sign in</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
            Enter your credentials to continue
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontSize: '13px', color: 'var(--text-sub)' }}>
              Username
            </label>
            <input
              id="username"
              type="text"
              placeholder="your username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              autoFocus
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontSize: '13px', color: 'var(--text-sub)' }}>
              Password
            </label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>

          {error && <p className="error">{error}</p>}

          <button
            id="login-submit"
            className="btn-primary"
            type="submit"
            disabled={loading}
            style={{ width: '100%', padding: '10px', marginTop: '4px', fontSize: '14px' }}
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '20px', color: 'var(--text-muted)', fontSize: '13px' }}>
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
