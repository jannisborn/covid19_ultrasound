import React, {useEffect} from 'react';
import gsap from "gsap";

const ScreenVideoResult = ({image, data, identifier}) => {

    let results = '';
    let colorClass = '';
    let url = ''

    useEffect(() => {
        let formData = new FormData();
        location.state.files.map((file) => {
            formData.append('image', file);
            fetch('/pyapi/video_predict', {
                method: 'POST',
                body: formData
            })
            .then(data => data.json())
            .then(data => {
                image.preview = URL.createObjectURL(image);
                res = JSON.parse(data.result.split("\n")[0]);
                url = data.result.split("\n")[1]
                
            
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
            
                let tl = gsap.timeline();
                useEffect(() => {
                    let el = '#key-' + identifier;
                    tl.from(el, 1.2, {y: 80, opacity: 0, ease: 'power4.out'})
                }, [identifier]);
            })
        });
    }, [location]);




    return (
        <div id={`key-${identifier}`} className={`result ${colorClass} d-md-flex mb-5`}>
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
                <div className="result-information-part video">
                    <h3 className="mt-4">Heatmap</h3>
                    <video width="400" controls>
                        <source src={url} type="video/mp4"></source>
                    </video>
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

export default ScreenVideoResult;
