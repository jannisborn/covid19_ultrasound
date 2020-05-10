import {useIntersection} from 'react-use';
import gsap from "gsap";

export function useFadeInOnScroll(ref) {
    const threshold = .45;
    const onScreen = useIntersection(ref, {
        root: null,
        rootMargin: '0px',
        threshold: threshold
    });

    const fadeIn = (el) => {
        gsap.to(el, .67, {opacity: 1, y: -30, stagger: {amount: .6}, ease: 'power4.out'})
    };

    if (ref.current && onScreen && onScreen.intersectionRatio >= threshold) {
        fadeIn(ref.current.querySelectorAll('.fadeIn'));
    }
}
