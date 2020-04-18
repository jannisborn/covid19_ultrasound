import React from 'react';
import './footer.scss';
import Logo from '../Logo/Logo';

const Footer = () => {

    return (
        <footer className="app-footer pt-5">
            <div className="container mb-4">
                <div className="row">
                    <div className="col-md-6 col-lg-5">
                        <Logo/>
                        <p>POCUS, X-Ray and CT's image analysis through AI to screen COVID-19 and pneumonia or healthy people.</p>
                    </div>
                    <div className="col-md-6 col-lg-5 offset-lg-2">
                        <div className="row">
                            <div className="col">
                                <h3>Legal</h3>
                                <ul className="app-footer-links">
                                    <li>Data privacy</li>
                                    <li>Terms of service</li>
                                </ul>
                            </div>
                            <div className="col offset-1">
                                <h3>Handy links</h3>
                                <ul className="app-footer-links">
                                    <li>Credits</li>
                                    <li>Disclaimer</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="copyright py-2">
                <div className="container">
                    <div className="row justify-content-between">
                        <div className="col">© Copyright {(new Date().getFullYear())}</div>
                        <div className="col text-right">A #CodeVsCovid19 project</div>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
