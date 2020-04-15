import React from 'react';
import './content.scss';

const TextSimple = (props) => {
    return (
        <>
            <header>
                <h2 className="fadeIn">{props.title}</h2>
                {props.subtitle &&
                    <p className="fadeIn">{props.subtitle}</p>
                }
            </header>
            <p className="fadeIn">{props.text}</p>
        </>
    );
};

export default TextSimple;
