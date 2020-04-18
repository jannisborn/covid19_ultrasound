import React, {useRef} from 'react';
import './statistic-number.scss';
import {useFadeInOnScroll} from '../Animation/Utils';
import StatisticNumber from './StatisticNumber';

const StatisticNumberList = (props) => {

    const statsRef = useRef(null);
    useFadeInOnScroll(statsRef);

    return (
        <div className="row" ref={statsRef}>
            <div className="col-8 col-md offset-lg-1 fadeIn">
                <StatisticNumber className="primary" number="3682" text="COVID-19 cases detected by the AI."/>
            </div>
            <div className="col-8 col-md fadeIn">
                <StatisticNumber className="secondary" number="12508" text="images that trained the AI."/>
            </div>
            <div className="col-8 col-md fadeIn">
                <StatisticNumber className="primary" number="50" text="organisations collaborating with us."/>
            </div>
        </div>
    );
};

export default StatisticNumberList;
