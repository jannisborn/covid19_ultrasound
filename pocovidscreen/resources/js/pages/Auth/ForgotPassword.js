import React, {useState} from 'react';
import Layout from '../Layout';
import {Helmet} from 'react-helmet';
import configuration from '../../utils/constants';
import Teaser from '../../components/Teaser/Teaser';
import {forgotPassword} from '../../api/auth';
import useInputValue from '../../utils/input-value';

const ForgotPassword = () => {
    let [resetFeedback, setResetFeedback] = useState('');
    let email = useInputValue('email');

    const handleSubmit = e => {
        e.preventDefault();

        console.log(email.value);
        forgotPassword({ email: email.value })
            .then(status => setResetFeedback(status))
            .catch(error => {
                error.json().then(({errors}) => {
                    email.parseServerError(errors);
                });
            });
    };

    return (
        <Layout>
            <Helmet>
                <title>{configuration.appTitle} - Forgot password</title>
            </Helmet>
            <Teaser additionalClass="small" teaser="Fill in the form to login"/>
            <div className="container">
                <div className="row">
                    <div className="col-lg-8 offset-lg-2 col-xl-6 offset-xl-3">
                        <form onSubmit={handleSubmit} className="form p-5">
                            <h2 className="text-center mb-5">Sign in</h2>
                            <div className="mb-4">
                                <label htmlFor="email">Enter your email address</label>
                                <input id="email" name="email" type="email" className="w-100" placeholder="example@domain.com" {...email.bind}/>
                                { email.error && <p className="text-red-500 text-xs">{ email.error }</p> }
                            </div>
                            <button className="button primary round w-100 text-uppercase mt-4">Reset password</button>
                        </form>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default ForgotPassword;
