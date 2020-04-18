import React from 'react';
import {useIntl} from 'react-intl';
import './statistic-number.scss';

const StatisticNumber = (props) => {
    const intl = useIntl();
    const numberFormat = (value) =>
        new Intl.NumberFormat(intl.locale, {
            style: 'decimal'
        }).format(value);

    return (
        <div className={`statistic-number ${props.className} pt-5`}>
            <h3>{numberFormat(props.number)}</h3>
            <p>{props.text}</p>
        </div>
    );
};

export default StatisticNumber;
