import React from 'react';
import {useLocation} from 'react-router-dom';
import Layout from '../Layout';
import {Helmet} from 'react-helmet';
import Teaser from '../../components/Teaser/Teaser';

const SignIn = () => {

    const location = useLocation();

    return (
        <Layout>
            <Helmet>
                <title>PocovidScreen - Home</title>
            </Helmet>
            <Teaser teaser="Fill in the form to login"/>
        </Layout>
    );
};

export default SignIn;
