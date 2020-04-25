import React, {useRef} from 'react';
import hidora from './images/hidora.png'
import google from './images/google.svg'
import euvsvirus from './images/euvsvirus.svg'
import {useFadeInOnScroll} from '../../utils/animation';

const PartnerList = () => {

    const partnersRef = useRef(null);
    useFadeInOnScroll(partnersRef);

    return (
        <div className="row align-items-center justify-content-between pt-2" ref={partnersRef}>
            <a href="https://hidora.com/" target="_blank" className="partner col fadeIn my-4" title="Visit the website of our fantastic hosting sponsor.">
                <img src={hidora} alt="Hidora logo"/>
            </a>
            <a href="https://euvsvirus.org/" target="_blank" className="partner col fadeIn my-4">
                <img src={euvsvirus} alt="The EUvsVirus logo" width="180"/>
            </a>
            <a href="https://www.google.com/" target="_blank" className="partner col fadeIn my-4">
                <img src={google} alt="Google logo"/>
            </a>
        </div>
    );
};

export default PartnerList;
