import React from 'react';

const TextSimple = (props) => {

    return (
        <>
            <header>
                {props.subtitle &&
                <p className="fadeIn mb-0">{props.subtitle}</p>
                }
                <h2 className="fadeIn mb-4">{props.title}</h2>
            </header>
            <p className="fadeIn">{props.text}</p>
        </>
    );
};

export default TextSimple;
