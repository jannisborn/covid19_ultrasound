import React from 'react';
import {Route, Switch, useHistory, useLocation} from 'react-router-dom';
import Layout from '../Layout';
import {Helmet} from 'react-helmet';
import configuration from '../../utils/constants';
import TextSimple from '../../components/Content/TextSimple';

const About = () => {

    return (
        <Layout>
            <Helmet>
                <title>{configuration.appTitle} - About</title>
            </Helmet>
            <div className="spacer-small">
                <div className="container">
                    <div className="text row mb-5">
                        <div className="col-8 col-lg-8 col-xl-6 offset-lg-1">
                            <header>
                                <h2 className="mb-4">Test</h2>
                            </header>
                            <p>The COVID-19 pandemic raises many new challenges to which we have to furnish fast
                                and innovative solutions. Especially the development of fast and reliable testing
                                methods are crucial to prevent the spread.
                                However, during the initial stages of the infection, viral RNA detection has been
                                questioned for its low sensitivity. In these cases, lung imaging becomes central to
                                screen patients presenting symptoms or with suspicions of contact with infected. While
                                CT imaging is already in use, several studies have now proven the applicability of
                                ultrasound recordings for diagnosis. Point-of-care ultrasound (POCUS) imaging is
                                by far preferable, because (in contrast to CT or X-rays) ultrasound imaging is an
                                easy, cost-effective, and non-invasive method of testing available in almost any medical
                                facility.
                                We develop the first approach for the automated detection of COVID-19 on
                                ultrasound recordings. Our machine learning model called POCOVID-Net, a
                                convolutional neural network, is able to distinguish between pneumonia, healthy and
                                covid with an accuracy of 89%. In particular, it detects COVID-19 with a sensitivity of
                                96% a specificity of 79% and a FI score of 92% in a 5-fold cross-validation test. Click
                                SCREEN (link to screen part of website) to test our model with your own data, or check
                                out the code on https://github.com/jannisborn/covid19_pocus_ultrasound
                                In order to turn this approach into an actual diagnosis tool to fight COVID-19, we need
                                your help! Contribute to our work with your own image or video data, or simply share
                                our website, so that we can together collect a large dataset and make it available to the
                                community!</p>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default About;
