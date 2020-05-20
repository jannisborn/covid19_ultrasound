import React, {useContext, useEffect, useRef} from 'react';
import TeamMember from '../TeamMember/TeamMember';
import {TweenLite, Power3} from 'gsap';
import chevronRightLight from './chevron-right.svg';
import chevronLeftLight from './chevron-left.svg';
import chevronRightDark from './chevron-right-dark.svg';
import chevronLeftDark from './chevron-left-dark.svg';
import {AppContext} from '../../context/AppContext';
import julie from '../../images/team/julie.jpg';
import marion from '../../images/team/marion.jpg';
import gabriel from '../../images/team/gabriel.jpg';
import manuel from '../../images/team/manuel.jpg';
import nina from '../../images/team/nina.jpg';
import janis from '../../images/team/janis.jpg';
import jay from '../../images/team/jay.jpg';
import lorenzo from '../../images/team/lorenzo.jpg';
import saheli from '../../images/team/saheli.jpg';

const Slider = () => {

    const context = useContext(AppContext);
    const isLight = context.themeMode === 'light';

    let chevronLeft = chevronLeftDark;
    let chevronRight = chevronRightDark;
    if (isLight) {
        chevronLeft = chevronLeftLight;
        chevronRight = chevronRightLight;
    }

    const sliderWrapRef = useRef(null);
    let sliderRef = useRef(null);
    let selectedIndex = 0;
    let cardWidth;
    let selected;

    useEffect(() => {
        TweenLite.to(
            [sliderRef.children[selectedIndex], sliderRef.children[selectedIndex + 1], sliderRef.children[selectedIndex + 2]],
            .7,
            {opacity: 1, ease: Power3.easeOut}
        );
    }, [selectedIndex]);

    const slideRight = () => {
        TweenLite.to(sliderRef.children, .7, {opacity: .3, ease: Power3.easeOut});
        cardWidth = sliderRef.firstElementChild.clientWidth;
        if (selectedIndex < (sliderRef.children.length - 1)) {
            selectedIndex++;
            TweenLite.to(sliderRef, .7, {x: -selectedIndex * cardWidth, ease: Power3.easeOut});
        }
        selected = [sliderRef.children[selectedIndex], sliderRef.children[selectedIndex + 1], sliderRef.children[selectedIndex + 2]]
        TweenLite.to(selected, .7, {opacity: 1, ease: Power3.easeOut});
    };

    const slideLeft = () => {
        TweenLite.to(sliderRef.children, .7, {opacity: .3, ease: Power3.easeOut});
        cardWidth = sliderRef.firstElementChild.clientWidth;
        if (selectedIndex > 0) {
            selectedIndex--;
            TweenLite.to(sliderRef, .7, {x: -selectedIndex * cardWidth, ease: Power3.easeOut});
        }
        selected = [sliderRef.children[selectedIndex], sliderRef.children[selectedIndex + 1], sliderRef.children[selectedIndex + 2]]
        TweenLite.to(selected, .7, {opacity: 1, ease: Power3.easeOut});
    };

    return (
        <div className="slider" ref={sliderWrapRef}>
            <div className="slider-cards" ref={el => sliderRef = el}>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Manuel Cossio" job="Medical Geneticist" image={manuel}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Marion Disdier" job="Data Scientist" image={marion}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Gabriel Brändle" job="Medical Doctor" image={gabriel}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Jannis Born" job=" Deep learning Expert" image={janis}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Julie Goulet" job="Theoretical biophysicist & Data Scientist" image={julie}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Jérémie Roulin" job="Software Engineer" image={jay}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Nina Wiedemann" job="Neuroscientist & Data Scientist" image={nina}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Lorenzo Carotenuto" job="UI/UX & Motion Designer" image={lorenzo}/>
                </div>
                <div className="slide-card col-6 col-md-4 fadeIn">
                    <TeamMember fullName="Saheli De" job="AI Expert" image={saheli}/>
                </div>
            </div>
            <div className="controls d-flex justify-content-between">
                <button className="left" onClick={slideLeft}><img src={chevronRight} alt=""/></button>
                <button className="right" onClick={slideRight}><img src={chevronLeft} alt=""/></button>
            </div>
        </div>
    );
};

export default Slider;
