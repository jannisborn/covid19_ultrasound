import React, {useEffect} from 'react';
import Text from '../../components/Content/Text';
import TextImage from '../../components/Content/TextImage';
import CallToAction from '../../components/CallToAction/CallToAction';
import gsap from 'gsap';
import VideoPresentation from '../../components/VideoPresentation/VideoPresentation';
import {Helmet} from 'react-helmet';
import Footer from '../../components/Footer/Footer';
import Slider from '../../components/Slider/Slider';
import StatisticList from '../../components/StatisticNumber/StatisticList';
import PartnerList from '../../components/Partner/ParternList';

const Home = () => {
    document.title = 'PocovidScreen - Home';

    let tl = gsap.timeline();
    useEffect(() => {
        gsap.to('.page', 0, {visibility: 'visible'});
        tl.from('.teaser-wrapper', 1.5, {y: 500, opacity: 0, ease: 'power4.out'}, .25)
            .from('.teaser', 1.95, {scale: 2.5, autoRound: false, ease: 'power4.out'}, .05)
            .from('.teaser-text h1', .7, {y: 20, opacity: 0, ease: 'power4.out'}, 1.2)
            .from('.teaser-text p', .7, {y: 20, opacity: 0, ease: 'power4.out'}, 1.45)
            .from('.screen', .65, {y: 200, opacity: 0, ease: 'power4.out'}, 1.7)
            .from('.train', .65, {y: 200, opacity: 0, ease: 'power4.out'}, 1.95);

    });

    return (
        <div className="page page-home">
            <Helmet>
                <title>PocovidScreen - Home</title>
            </Helmet>
            <section className="text-center container-fluid">
                <div className="teaser-wrapper">
                    <div className="teaser">
                        <div className="teaser-text col-12 col-lg-8 col-xl-6">
                            <header>
                                <h1>PocovidScreen</h1>
                                <p>POCUS, X-Ray and CT's image analysis through AI to screen COVID-19 and pneumonia or healthy people</p>
                            </header>
                        </div>
                    </div>
                </div>
            </section>
            <section className="start container">
                <div className="row">
                    <div className="screen col-10 offset-1 col-sm-12 mb-5 mb-md-0 offset-sm-0 col-md-6 col-lg-5 offset-lg-1">
                        <CallToAction action="/screen" title="Screen" text="Use our AI to detect COVID-19, pneumonia or healthy patient from POCUS, X-Ray or CT's images." linkTitle="Start screening" className="primary"/>
                    </div>
                    <div className="train col-10 offset-1 col-sm-12 offset-sm-0 col-md-6 col-lg-5">
                        <CallToAction action="/train" title="Train the AI" text="Send us your POCUS, X-Ray and CT's images to train our AI about COVID-19, pneumonia or healthy patient." linkTitle="Start training" className="secondary"/>
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <Text title="Our partners" text="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, veniam, voluptatem? Assumenda at beatae culpa doloremque, id ipsam nesciunt nulla, porro qui quibusdam similique, ut? Incidunt magnam nobis porro veritatis?"/>
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <PartnerList/>
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <Text title="Statistics" text="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, veniam, voluptatem? Assumenda at beatae culpa doloremque, id ipsam nesciunt nulla, porro qui quibusdam similique, ut? Incidunt magnam nobis porro veritatis?"/>
                <StatisticList/>
            </section>
            <section className="container spacer pb-3">
                <VideoPresentation title="Presentation video" videoId="cVFzblT5VPE"/>
            </section>
            <section className="container spacer pt-4">
                <Text title="The team" text="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, veniam, voluptatem? Assumenda at beatae culpa doloremque, id ipsam nesciunt nulla, porro qui quibusdam similique, ut? Incidunt magnam nobis porro veritatis?"/>
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <Slider/>
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <TextImage orientation="textLeft" title="Your title" subtitle="Subtitle" text="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, veniam, voluptatem? Assumenda at beatae culpa doloremque."/>
                    </div>
                </div>
            </section>
            <section className="container spacer">
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <TextImage title="Your title" subtitle="Subtitle" text="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, veniam, voluptatem? Assumenda at beatae culpa doloremque."/>
                    </div>
                </div>
            </section>
            <Footer/>
        </div>
    );
};

export default Home;
