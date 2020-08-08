import React, { useContext, useEffect, useState } from 'react';
import Text from '../../components/Content/Text';
import TextImage from '../../components/Content/TextImage';
import CallToAction from '../../components/CallToAction/CallToAction';
import gsap from 'gsap';
import covid from '../../assets/images/covid19.png'
import pocus from '../../assets/images/pocus-covid.gif'
import VideoPresentation from '../../components/VideoPresentation/VideoPresentation';
import { Helmet } from 'react-helmet';
import Slider from '../../components/Slider/Slider';
import StatisticList from '../../components/StatisticNumber/StatisticList';
import PartnerList from '../../components/Partner/ParternList';
import Layout from '../Layout';
import Teaser from '../../components/Teaser/Teaser';
import configuration from '../../utils/constants';
import Modal from '../../components/Modal/Modal';
import { acceptDisclaimer, AppContext } from '../../context/AppContext';
import { useHistory } from 'react-router-dom';

const Home = () => {

    const [modalOpened, setModalOpened] = useState(false);
    const context = useContext(AppContext);
    const history = useHistory();

    const showDisclaimerModal = () => {
        if (context.disclaimerAccepted) {
            history.push('/screen');
        } else {
            setModalOpened(true);
        }
    };

    const showDisclaimerModalVideo = () => {
        if (context.disclaimerAccepted) {
            history.push('/screenvideo');
        } else {
            setModalOpened(true);
        }
    };

    const hideDisclaimerModal = () => {
        setModalOpened(false);
    };

    const startScreening = () => {
        acceptDisclaimer();
        history.push('/screen');
    };

    let tl = gsap.timeline();
    useEffect(() => {
        gsap.to('.page', 0, { visibility: 'visible' });
        tl.from('.teaser-wrapper', 1.5, { y: 500, opacity: 0, ease: 'power4.out' }, .25)
            .from('.teaser', 1.95, { scale: 2.5, autoRound: false, ease: 'power4.out' }, .05)
            .from('.teaser-text h1', .7, { y: 20, opacity: 0, ease: 'power4.out' }, 1.2)
            .from('.teaser-text p', .7, { y: 20, opacity: 0, ease: 'power4.out' }, 1.45)
            .from('.screen', .65, { y: 200, opacity: 0, ease: 'power4.out' }, 1.7)
            .from('.train', .65, { y: 200, opacity: 0, ease: 'power4.out' }, 1.95);
    }, []);

    return (
        <Layout className="page">
            <Helmet>
                <title>Home - {configuration.appTitle}</title>
            </Helmet>
            <Teaser teaser="An AI tool for interpretable screening of COVID-19 and other forms of pneumonia from (point-of-care) lung ultrasound (POCUS/LUS)" />
            <section className="start container">
                <div className="row">
                    <div
                        className="screen col-10 offset-1 col-sm-12 mb-5 mb-md-0 offset-sm-0 col-md-6 col-lg-5 offset-lg-1">
                        <CallToAction onClick={showDisclaimerModal} title="Screen"
                            text="Use our AI on your LUS data to screen for COVID-19, pneumonia or healthy lungs."
                            linkTitle="Start screening" className="primary" />
                    </div>
                    <div className="train col-10 offset-1 col-sm-12 offset-sm-0 col-md-6 col-lg-5">
                        <CallToAction action="/train" title="Donate your data"
                            text="Send us your LUS recordings to train and improve our AI."
                            linkTitle="Start training" className="secondary" />
                    </div>
                </div>
                <div className="row">
                    <div
                        className="screen col-10 offset-1 col-sm-12 mb-5 mb-md-0 offset-sm-0 col-md-6 col-lg-5 offset-lg-1">
                        <CallToAction onClick={showDisclaimerModalVideo} title="Screen Video"
                            text="Use our AI to detect COVID-19, pneumonia or healthy patient from POCUS videos and view a heatmap of what the AI sees."
                            linkTitle="Start video screening" className="primary" />
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <Text title="Our sponsors"
                    text="We would like to deeply thank all of our sponsors. We received support in web hosting, data collection, promotion and more." />
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <PartnerList />
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <Text title="Statistics"
                    text="Here are some statistics about our infrastructure, the performance on COVID-19 and the size of our dataset." />
                <StatisticList />
            </section>
            <section className="container spacer pb-3">
                <VideoPresentation title="Presentation video" videoId="qOayWwYTPOs" />
            </section>
            <section className="container spacer pt-4">
                <Text title="The team"
                    text="We are an interdisciplinary team of doctors, scientists and developers. Everyone brought major contribution to this project and we believe we found something that could actually help COVID-19 detection and therefore improve treatments when given at early stage." />
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <Slider />
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <TextImage orientation="textLeft" title="Early screening" subtitle="The impact" image={covid}
                            text="In a global pandemic, early screening and rapid patient stratification is crucial to save lives." />
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <TextImage title="Why POCUS?" subtitle="Focusing" image={pocus}
                            text="We focused on POCUS data, because ultrasound imaging is an easy, cost-effective and non-invasive method. It is available in almost any medical facility. Our model can identify with a 98% sensitivity and 91% specificity COVID-19 cases." />
                    </div>
                </div>
            </section>
            <Modal show={modalOpened} handleClose={hideDisclaimerModal}>
                <h2>Disclaimer</h2>
                <p>
                    We highly recommend to follow approved clinical guidelines for the diagnosis and management of
                    COVID-19. By no means you should base your clinical decision solely on the result of this algorithm.
                    You should also read carefully our <a href="/terms-and-conditions">terms and conditions</a>.
                </p>
                <button type="button" onClick={startScreening} className="button primary round mt-4 px-5">Agree</button>
            </Modal>
        </Layout>
    );
};

export default Home;
