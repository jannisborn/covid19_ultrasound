import 'whatwg-fetch';
import {getToken} from '../utils/auth';
import NProgress from 'nprogress';
let requestsCounter = 0;

function Client (endpoint, {method, body, ...customConfig} = {}) {
  const token = getToken();

  const headers = {
    'content-type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  method = method || (body ? 'POST' : 'GET');

  const config = {
    method,
    ...customConfig,
    headers: {
      ...headers,
      ...customConfig.headers
    }
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  if (method === 'GET') {
    requestsCounter++;
    NProgress.start();
  }

  return window
    .fetch(endpoint, config)
    .then(r => {
      if (r.status >= 200 && r.status < 300) {
        if ((--requestsCounter) === 0) {
          NProgress.done();
        }
        return r.json();
      }

      return Promise.reject(r);
    }).catch(error => {
      if (requestsCounter > 0 && ((--requestsCounter) === 0)) {
        NProgress.done();
      }
      return Promise.reject(error);
    });
}

export default Client;
