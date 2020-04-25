import React, {useRef} from 'react';
import TextSimple from './TextSimple';
import {useFadeInOnScroll} from '../../utils/animation';

const Text = (props) => {

    const sectionRef = useRef(null);
    useFadeInOnScroll(sectionRef);

    return (
        <div className="text row mb-5" ref={sectionRef}>
            <div className="col-8 col-lg-8 col-xl-6 offset-lg-1">
                <TextSimple title={props.title} subtitle={props.subtitle} text={props.text}/>
            </div>
        </div>
    );
};

export default Text;
