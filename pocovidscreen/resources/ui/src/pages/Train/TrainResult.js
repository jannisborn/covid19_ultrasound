import React from 'react';
import Layout from '../Layout';
import Text from '../../components/Content/Text';
import {useLocation} from 'react-router-dom';

const TrainResult = (props) => {

    const location = useLocation();

    return (
        <Layout>
            <div className="container spacer">
                <Text title="Thanks for training the AI"
                      text="We really appreciate your donation."/>
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <a href="/train" title="Train the AI again" className="button primary round w-100 text-uppercase mt-4 d-block text-center">Train the AI again</a>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default TrainResult;
