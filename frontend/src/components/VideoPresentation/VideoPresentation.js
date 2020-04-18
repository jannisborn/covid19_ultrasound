import React from 'react';
import './video-presentation.scss';

const VideoPresentation = (props) => {

    return (
        <div className="presentation-video pt-5 text-center">
            <h2>{props.title}</h2>
            <div className="row">
                <div className="col-10 offset-1">
                    <div className="presentation-video-thumbnail">
                        <img src={`https://img.youtube.com/vi/${props.videoId}/maxresdefault.jpg`} alt="Video thumbnail" className="img-fluid"/>
                        <a title="Watch our presentation video" href={`https://www.youtube.com/watch?v=${props.videoId}`} className="presentation-video-play d-block" target="_blank" rel="noopener noreferrer">
                            <span>&gt;</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default VideoPresentation;
