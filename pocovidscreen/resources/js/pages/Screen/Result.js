import React, {useEffect} from 'react';

const Result = ({image, data}) => {

    let results = 'Test'
    let probability = '95%'
    let additionalClass = 'high'

    return (
        <div className={`result ${additionalClass}`}>
            <div className="result-image">
                <img src={image.preview} alt={`Result for ${image.path}`}/>
            </div>
            <div className="result-information">
                <div className="result-information-part image-title">
                    <h3>Title</h3>
                    <p>{image.path}</p>
                </div>
                <div className="result-information-part symptoms">
                    <h3>Results</h3>
                    <p className="result-text">{results}</p>
                </div>
                <div className="result-information-part probability">
                    <h3>Probability</h3>
                    <div className="progress">
                        <div className="progress-size"></div>
                    </div>
                    <p className="result-probability">{probability}</p>
                </div>
            </div>
        </div>
    );
};

export default Result;
