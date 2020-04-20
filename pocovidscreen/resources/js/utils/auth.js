const authToken = 'auth_token';
const intendedUrl = 'intendedUrl';
const defaultIntendedUrl = '/home';

export const getToken = () => window.localStorage.getItem(authToken);

export const setToken = token => {
  token
    ? window.localStorage.setItem(authToken, token)
    : window.localStorage.removeItem(authToken);
};

export const getIntendedUrl = () => window.localStorage.getItem(intendedUrl) || defaultIntendedUrl;

export const setIntendedUrl = url => {
  url
    ? window.localStorage.setItem(intendedUrl, url)
    : window.localStorage.removeItem(intendedUrl);
};
