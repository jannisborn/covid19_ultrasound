import React, {useRef} from 'react';
import hidora from './images/hidora.png'
import google from './images/google.svg'
import euvsvirus from './images/euvsvirus.svg'
import hackzurich from './images/hackzurich.jpg'
import backpack from './images/backpack.png'
import checkdomain from './images/checkdomain.svg'
import lumiata from './images/lumiata.svg'
import {useFadeInOnScroll} from '../../utils/animation';

const PartnerList = () => {

    const partnersRef = useRef(null);
    useFadeInOnScroll(partnersRef);

    return (
        <div className="row align-items-center justify-content-between pt-2" ref={partnersRef}>
            <a href="https://hidora.com/" target="_blank" className="partner col fadeIn my-4" title="Visit the website of our fantastic hosting sponsor.">
                <img src={hidora} alt="Hidora logo"/>
            </a>
            <a href="https://digitalfestival.ch/en/HACK/" target="_blank" className="partner col fadeIn my-4" title="Event website">
                <img src={hackzurich} alt="The Hack Zurich logo" width="90"/>
            </a>
            <a href="https://euvsvirus.org/" target="_blank" className="partner col fadeIn my-4" title="Event website">
                <img src={euvsvirus} alt="The EUvsVirus logo" width="160"/>
            </a>
            <a href="https://www.lumiata.com/" target="_blank" className="partner col fadeIn my-4" title="Event organizer website">
                <img src={lumiata} alt="The Lumiata logo" width="110"/>
            </a>
            <a href="https://www.google.com/" target="_blank" className="partner col fadeIn my-4" title="Our cloud hosting provider.">
                <img src={google} alt="Google logo"/>
            </a>
            <a href="https://backpackforlaravel.com/" target="_blank" className="partner col fadeIn my-4" title="Website of our backend provider.">
                <img src={backpack} alt="Backpack logo" width="180"/>
            </a>
            <a href="https://www.checkdomain.net/" target="_blank" className="partner col fadeIn my-4" title="Our sponsor for the domain name.">
                <img src={checkdomain} alt="Checkdomain logo"/>
            </a>
        </div>
    );
};

export default PartnerList;
