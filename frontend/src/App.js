import React from 'react';
import './theme.scss';
import {AppProvider} from './context/AppContext';
import Layout from './Layout';
import {IntlProvider} from 'react-intl';

const App = () => {
    return (
        <AppProvider>
            <IntlProvider locale="en-EN">
                <Layout/>
            </IntlProvider>
        </AppProvider>
    );
};

export default App;
