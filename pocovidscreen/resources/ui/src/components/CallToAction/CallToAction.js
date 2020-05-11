import React from 'react';

const CallToAction = (props) => {

    return (
        <a className={`call-to-action py-5 px-4 d-block ${props.className}`} href={props.action}
           title={props.linkTitle}>
            <h2>{props.title}</h2>
            <p>{props.text}</p>
            <p className="call-to-action-link mt-5 mb-0">{props.linkTitle}</p>
        </a>
    );
};

export default CallToAction;
