import React from 'react';

const Button = (props) => {

    return (
        <a className={`button ${props.className}`} href={props.href} title={props.title}>
            {props.text}
        </a>
    );
};

export default Button;
