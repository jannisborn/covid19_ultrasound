import React from 'react';
import configuration from '../../utils/constants';

const Footer = () => {

    return (
        <footer className="app-footer pt-5">
            <div className="container mb-4">
                <div className="row">
                    <div className="col-lg-5 mb-5 mb-lg-0">
                        <h2 className="mb-1">{configuration.appTitle}</h2>
                        <p>POCUS image analysis through AI to screen COVID-19 and pneumonia or healthy people.</p>
                    </div>
                    <div className="col-lg-6 col-xl-5 offset-xl-2 offset-lg-1">
                        <div className="row">
                            <div className="col">
                                <h3 className="mb-4">Legal</h3>
                                <ul className="app-footer-links">
                                    <li><a href="/data-privacy">Data privacy</a></li>
                                    <li><a href="/terms-and-conditions">Terms and conditions</a></li>
                                </ul>
                            </div>
                            <div className="col offset-1">
                                <h3 className="mb-4">Handy links</h3>
                                <ul className="app-footer-links">
                                    <li><a href="https://arxiv.org/abs/2004.12084" title="Read our scientific article" target="_blank">Scientific article</a></li>
                                    <li><a href="https://github.com/jannisborn/covid19_pocus_ultrasound" target="_blank" title="See code and data">GitHub repository</a></li>
                                    <li><a href="https://towardsdatascience.com/ultrasound-for-covid-19-a-deep-learning-approach-f7906002892a" target="_blank" title="Read our blog post">Blog post</a></li>
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
                        <div className="col text-right">A <a href="https://www.codevscovid19.org/" target="_blank"
                            title="Visit the official event page">#CodeVsCovid19</a>, <a href="https://euvsvirus.org/" target="_blank"
                                title="Visit the official event page">#EUvsVirus</a>  project
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
