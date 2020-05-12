import React from 'react';

const CallToAction = (props) => {

    return (
        props.action ? (
            <a className={`call-to-action py-5 px-4 d-block ${props.className}`} href={props.action}
               title={props.linkTitle}>
                <h2>{props.title}</h2>
                <p>{props.text}</p>
                <p className="call-to-action-link mt-5 mb-0">{props.linkTitle}</p>
            </a>
        ) : (
            <button className={`call-to-action py-5 px-4 d-block ${props.className}`} onClick={props.onClick}
               title={props.linkTitle}>
                <h2>{props.title}</h2>
                <p>{props.text}</p>
                <p className="call-to-action-link mt-5 mb-0">{props.linkTitle}</p>
            </button>
        )
    );
};

export default CallToAction;
