import React from 'react';
import {useIntl} from 'react-intl';

const StatisticNumber = (props) => {

    const intl = useIntl();

    return (
        <div className={`statistic-number ${props.className} pt-5`}>
            <h3>{props.number}</h3>
            <p>{props.text}</p>
        </div>
    );
};

export default StatisticNumber;
