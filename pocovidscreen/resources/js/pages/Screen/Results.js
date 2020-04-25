import React, {useEffect, useState} from 'react';
import Layout from '../Layout';
import Text from '../../components/Content/Text';
import {useLocation} from 'react-router-dom';
import Result from './Result';

const Results = (props) => {


    const location = useLocation();

    useEffect(() => {
        console.log('called');
        console.log(location.state.results);
    });

    return (
        <Layout>
            <div className="container spacer">
                <Text title="Results"
                      text="We highly recommend to follow approved clinical guidelines for the diagnosis and management of COVID19. By any means you should base your clinical decision solely on the result of this algorithm."/>
            </div>
        </Layout>
    );
};

export default Results;
