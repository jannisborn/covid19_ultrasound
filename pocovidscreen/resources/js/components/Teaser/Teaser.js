import React from 'react';
import configuration from '../../utils/constants'

const Teaser = (props) => {
    return (
        <section className="text-center container-fluid">
            <div className={`teaser-wrapper ${props.additionalClass}`}>
                <div className="teaser">
                    <div className="teaser-text col-12 col-lg-8 col-xl-6">
                        <header>
                            <h1>PO<span className="text-blue">COVID</span>SCREEN</h1>
                            <p>{props.teaser}</p>
                        </header>
                    </div>
                </div>
            </div>
        </section>
    );
};

Teaser.defaultProps = {
    additionalClass: ''
}

export default Teaser;
