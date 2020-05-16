import React, {useRef} from 'react';
import {useFadeInOnScroll} from '../../utils/animation';
import StatisticNumber from './StatisticNumber';

const StatisticNumberList = (props) => {

    const statsRef = useRef(null);
    useFadeInOnScroll(statsRef);

    return (
        <div className="row pt-5" ref={statsRef}>
            <div className="col-8 col-md offset-lg-1 fadeIn">
                <StatisticNumber className="primary" number="64" text="videos edited by our data scientists."/>
            </div>
            <div className="col-8 col-md fadeIn">
                <StatisticNumber className="secondary" number="1103" text="images that trained the AI."/>
            </div>
            <div className="col-8 col-md fadeIn">
                <StatisticNumber className="primary" number="96%" text="sensititvity of our AI on COVID-19 cases."/>
            </div>
        </div>
    );
};

export default StatisticNumberList;
