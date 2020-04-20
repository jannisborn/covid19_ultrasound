import React from 'react';

const Footer = () => {

    return (
        <footer className="app-footer pt-5">
            <div className="container mb-4">
                <div className="row">
                    <div className="col-md-6 col-lg-5">
                        <h2 className="mb-1">CovidScreen</h2>
                        <p>POCUS, X-Ray and CT's image analysis through AI to screen COVID-19 and pneumonia or healthy people.</p>
                    </div>
                    <div className="col-md-6 col-lg-5 offset-lg-2">
                        <div className="row">
                            <div className="col">
                                <h3 className="mb-4">Legal</h3>
                                <ul className="app-footer-links">
                                    <li><a href="">Data privacy</a></li>
                                    <li>Terms of service</li>
                                </ul>
                            </div>
                            <div className="col offset-1">
                                <h3 className="mb-4">Handy links</h3>
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
                        <div className="col text-right">A <a href="https://www.codevscovid19.org/" target="_blank" title="Visit the official event page">#CodeVsCovid19</a> project</div>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
