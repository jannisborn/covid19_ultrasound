import ReactDOM from 'react-dom';
import { AuthProvider } from './context/AuthContext';
import React from 'react';
import {AppProvider} from './context/AppContext';
import Layout from './Layout';
import {IntlProvider} from 'react-intl';

ReactDOM.render(
    <AuthProvider>
        <AppProvider>
            <IntlProvider locale="en-EN">
                <Layout/>
            </IntlProvider>
        </AppProvider>
    </AuthProvider>,
  document.getElementById('app')
);
