import ReactDOM from 'react-dom';
import {AuthProvider} from './context/AuthContext';
import React from 'react';
import {AppProvider} from './context/AppContext';
import Frame from './Frame';
import {IntlProvider} from 'react-intl';
import './sass/app.scss'

ReactDOM.render(
    <AuthProvider>
        <AppProvider>
            <IntlProvider locale="en-EN">
                <Frame/>
            </IntlProvider>
        </AppProvider>
    </AuthProvider>,
    document.getElementById('root')
);
