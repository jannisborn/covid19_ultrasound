import React, {useRef, useState} from 'react';
import {useIntersection} from 'react-use';
import {TimelineLite} from "gsap";
import videoImage from '../../assets/images/video.png';
import play from './images/play.svg';

const VideoPresentation = (props) => {

    const videoRef = useRef(null);
    const [animated, setAnimated] = useState('initial');
    useAnimate(videoRef, animated, setAnimated);

    return (
        <div className="video-wrapper" ref={videoRef}>
            <div className="presentation-video o0 pt-5 text text-center">
                <h2 className="animated-title o0">{props.title}</h2>
                <div className="row">
                    <div className="col-10 offset-1">
                        <div className="presentation-video-thumbnail o0 animated-video">
                            <img src={videoImage}
                                 alt="Video thumbnail" className="img-fluid animated-image"/>
                            <a title="Watch our presentation video"
                               href={`https://www.youtube.com/watch?v=${props.videoId}`}
                               className="presentation-video-play d-block" target="_blank" rel="noopener noreferrer">
                                <img className="play" src={play}/>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

function useAnimate(ref, animated, setAnimated) {
    const threshold = .45;
    const onScreen = useIntersection(ref, {
        root: null,
        rootMargin: '0px',
        threshold: threshold
    });

    const animate = (wrapper, title, video, image) => {

        if (animated === 'initial') {
            let tl = new TimelineLite();
            tl.fromTo(wrapper, 1.67,
                {opacity: 0, y: 800, ease: 'power4.out'},
                {opacity: 1, y: 0, ease: 'power4.out'}
            ).fromTo(title, .87,
                {opacity: 0, y: 100, ease: 'power4.out'},
                {opacity: 1, y: 0, ease: 'power4.out'}, .4
            ).fromTo(video, 1.7,
                {opacity: 0, y: 90, ease: 'power4.out'},
                {opacity: 1, y: 50, ease: 'power4.out'}, .7
            ).fromTo(image, 1.78,
                {scale: 2.2, ease: 'power4.out'},
                {scale: 1, ease: 'power4.out'}, .6
            );
            setAnimated('animated');
        }

    };

    if (ref.current && onScreen && onScreen.intersectionRatio >= threshold) {
        animate(
            ref.current.querySelectorAll('.presentation-video'),
            ref.current.querySelectorAll('.animated-title'),
            ref.current.querySelectorAll('.animated-video'),
            ref.current.querySelectorAll('.animated-image')
        );
    }
}

export default VideoPresentation;
