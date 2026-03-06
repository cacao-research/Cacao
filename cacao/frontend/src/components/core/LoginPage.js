/**
 * LoginPage - Shown when auth is required but user is not authenticated
 */

const { createElement: h, useState, useCallback } = React;

export function LoginPage({ onLogin, title }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();

      if (data.success) {
        sessionStorage.setItem('cacao-auth-token', data.token);
        if (onLogin) onLogin(data);
      } else {
        setError(data.message || 'Invalid credentials');
      }
    } catch (err) {
      setError('Connection error');
    } finally {
      setLoading(false);
    }
  }, [username, password, onLogin]);

  return h('div', { className: 'login-page' },
    h('form', { className: 'login-form', onSubmit: handleSubmit }, [
      h('h2', { key: 'title', className: 'login-title' }, title || 'Sign In'),
      error && h('div', { key: 'error', className: 'login-error' }, error),
      h('div', { key: 'field-user', className: 'login-field' }, [
        h('label', { key: 'label', htmlFor: 'login-username' }, 'Username'),
        h('input', {
          key: 'input',
          id: 'login-username',
          type: 'text',
          value: username,
          onChange: (e) => setUsername(e.target.value),
          autoFocus: true,
          autoComplete: 'username',
          required: true,
        }),
      ]),
      h('div', { key: 'field-pass', className: 'login-field' }, [
        h('label', { key: 'label', htmlFor: 'login-password' }, 'Password'),
        h('input', {
          key: 'input',
          id: 'login-password',
          type: 'password',
          value: password,
          onChange: (e) => setPassword(e.target.value),
          autoComplete: 'current-password',
          required: true,
        }),
      ]),
      h('button', {
        key: 'submit',
        type: 'submit',
        className: 'login-submit',
        disabled: loading,
      }, loading ? 'Signing in...' : 'Sign In'),
    ])
  );
}
