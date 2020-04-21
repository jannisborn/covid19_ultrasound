import React, {useRef} from 'react';
import chuv from './images/chuv.svg'
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
            <div className="partner col fadeIn my-4">
                <img src={chuv} alt=""/>
            </div>
            <div className="partner col fadeIn my-4">
                <img src={hug} alt=""/>
            </div>
            <div className="partner col fadeIn my-4">
                <img src={oms} alt=""/>
            </div>
            <div className="partner col fadeIn my-4">
                <img src={epfl} alt=""/>
            </div>
            <div className="partner col fadeIn my-4">
                <img src={google} alt=""/>
            </div>
        </div>
    );
};

export default PartnerList;
