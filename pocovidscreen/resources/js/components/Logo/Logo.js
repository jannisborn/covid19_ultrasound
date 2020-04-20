import React from 'react';
import logoSmall from './logo-small.svg'
import logoBig from './logo-big.svg'

const Logo = (props) => {

    let src = logoSmall;
    if (props.size === 'big') {
        src = logoBig;
    }

    return (
        <div className={`logo logo-${props.size}`}><img src={src} alt="CovidScreen logo"/></div>
    );
};

export default Logo;
