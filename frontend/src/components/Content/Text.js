import React, {useRef} from 'react';
import './content.scss';
import TextSimple from './TextSimple';
import {useIntersection} from 'react-use';
import gsap from "gsap";
import {useFadeInOnScroll} from '../Animation/Utils';

const Text = (props) => {

    const sectionRef = useRef(null);
    useFadeInOnScroll(sectionRef);

    return (
        <div className="text row mb-5" ref={sectionRef}>
            <div className="col-8 col-lg-6 col-xl-5 offset-lg-1">
                <TextSimple title={props.title} subtitle={props.subtitle} text={props.text}/>
            </div>
        </div>
    );
};

export default Text;
