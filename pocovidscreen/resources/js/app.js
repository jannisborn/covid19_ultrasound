import ReactDOM from 'react-dom';
import { AuthProvider } from './context/AuthContext';
import React from 'react';
import {AppProvider} from './context/AppContext';
import Layout from './Layout';
import {IntlProvider} from 'react-intl';

ReactDOM.render(
    <AppProvider>
        <IntlProvider locale="en-EN">
            <Layout/>
        </IntlProvider>
    </AppProvider>,
  document.getElementById('app')
);
