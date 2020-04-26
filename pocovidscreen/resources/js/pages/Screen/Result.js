import React, {useEffect} from 'react';

const Result = ({image, data}) => {

    let results = '';
    let colorClass = '';

    image.preview = URL.createObjectURL(image);
    const res = JSON.parse(data.result)
    const maxValueIndex = res.indexOf(Math.max(...res));
    const probability = Math.round(res[maxValueIndex] * 100);

    switch (maxValueIndex) {
        case 0:
            results = 'COVID-19 symptoms';
            break;
        case 1:
            results = 'Pneumonia symptoms';
            break;
        case 2:
            results = 'Healthy';
            break;
    }

    if (probability >= 0 && probability < 50) {
        colorClass = 'red';
    } else if (probability >= 50 && probability < 80) {
        colorClass = 'orange';
    } else {
        colorClass = 'green';
    }

    return (
        <div className={`result ${colorClass} d-md-flex mb-5`}>
            <div className="result-image">
                <img src={image.preview} alt={`Result for ${image.path}`}/>
            </div>
            <div className="result-information align-self-center px-5 py-4 mt-md-0 w-100">
                <div className="result-information-part image-title">
                    <h3>Title</h3>
                    <p>{image.path}</p>
                </div>
                <div className="result-information-part symptoms">
                    <h3 className="mt-4">Results</h3>
                    <p className="result-text">{results}</p>
                </div>
                <div className="result-information-part probability no-border">
                    <h3 className="mt-4">Probability</h3>
                    <div className="progress my-3">
                        <div className="progress-size" style={{width: `${probability}%`}}></div>
                    </div>
                    <p className="result-probability">{probability}&#37;</p>
                </div>
            </div>
        </div>
    );
};

export default Result;
