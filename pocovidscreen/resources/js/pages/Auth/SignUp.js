import React from 'react';
import Layout from '../Layout';
import {Helmet} from 'react-helmet';
import Teaser from '../../components/Teaser/Teaser';
import CallToAction from '../../components/CallToAction/CallToAction';

const SignUp = () => {

    return (
        <Layout>
            <Teaser additionalClass="small" teaser="Choose an option"/>
            <section className="sign-up container">
                <div className="row">
                    <div className="screen col-10 offset-1 col-sm-12 mb-5 mb-md-0 offset-sm-0 col-md-6 col-lg-5 offset-lg-1">
                        <CallToAction action="/sign-up" title="Register as an independent"
                                      text="Register as independent to be able to train our AI by sending labeled images."
                                      linkTitle="Register" className="primary"/>
                    </div>
                    <div className="train col-10 offset-1 col-sm-12 offset-sm-0 col-md-6 col-lg-5">
                        <CallToAction action="/sign-up" title="Register as an organisation"
                                      text="Grant access to the person of your choice in your organisation to allow them to tain our AI."
                                      linkTitle="Register" className="secondary"/>
                    </div>
                </div>
            </section>
        </Layout>
    );
};

export default SignUp;
