import React, {useRef} from 'react';
import hidora from './images/hidora.png'
import oms from './images/oms.svg'
import hug from './images/hug.svg'
import google from './images/google.svg'
import epfl from './images/epfl.svg'
import {useFadeInOnScroll} from '../../utils/animation';

const PartnerList = () => {

    const partnersRef = useRef(null);
    useFadeInOnScroll(partnersRef);

    return (
        <div className="row align-items-center justify-content-between pt-2" ref={partnersRef}>
            <a href="https://hidora.com/" target="_blank" className="partner col fadeIn my-4" title="Visit the website of our fantastic hosting sponsor.">
                <img src={hidora} alt="Hidora logo"/>
            </a>
            <a className="partner col fadeIn my-4">
                <img src={hug} alt=""/>
            </a>
            <a className="partner col fadeIn my-4">
                <img src={oms} alt=""/>
            </a>
            <a className="partner col fadeIn my-4">
                <img src={epfl} alt=""/>
            </a>
            <a className="partner col fadeIn my-4">
                <img src={google} alt=""/>
            </a>
        </div>
    );
};

export default PartnerList;
