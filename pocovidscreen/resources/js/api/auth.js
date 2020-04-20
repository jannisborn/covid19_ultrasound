import client from './client';

export const login = ({ email, password }) => {
  return client('/api/login', { body: { email, password } })
    .then(({ data: user, meta: { token } }) => {
      return { user, token };
    });
};

// eslint-disable-next-line camelcase
export const register = ({ email, name, password, password_confirmation }) => {
  return client('/api/register', { body: { email, name, password, password_confirmation } }
  ).then(({ data: user, meta: { token } }) => {
    return { user, token };
  });
};

export const forgotPassword = ({ email }) => {
  return client('/api/password/email', { body: { email } })
    .then(({ status }) => status);
};

// eslint-disable-next-line camelcase
export const resetPassword = ({ token, email, password, password_confirmation }) => {
  return client('/api/password/reset', { body: { token, email, password, password_confirmation } })
    .then(({ status }) => status);
};

export const logout = () => {
  return client('/api/logout', { body: {} });
};

export const getUser = () => {
  return client('/api/me')
    .then(({ data }) => data)
    .catch(() => null);
};
