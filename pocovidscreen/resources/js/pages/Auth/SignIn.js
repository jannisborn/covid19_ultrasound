import React from 'react';
import {useLocation} from 'react-router-dom';
import Layout from '../Layout';

const SignIn = () => {

    const location = useLocation();

    return (
        <Layout>
            <div className="container">Hello sign in</div>
        </Layout>
    );
};

export default SignIn;
