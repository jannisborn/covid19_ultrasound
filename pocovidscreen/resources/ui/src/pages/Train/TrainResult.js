import React, {useEffect, useState} from 'react';
import Layout from '../Layout';
import {useLocation} from 'react-router-dom';

const TrainResult = () => {

    const location = useLocation();
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let formData = new FormData();
        location.state.files.map((file) => {
            formData.append('image', file);
            formData.append('label', location.state.label);
            fetch('/api/train', {
                method: 'POST',
                body: formData
            })
                .then(data => data.json())
                .then(data => {
                    setLoading(false);
                    let preview = URL.createObjectURL(file);
                    setResults(results => results.concat({image: file, data: data, preview: preview}));
                })
        });
    }, [location]);

    return (
        <Layout>
            <div className="container spacer-small">
                <div className="row">
                    <div className="col-lg-8 offset-lg-2">
                        <div className="text-center">
                            <h2>Thanks for training the AI</h2>
                            <p className="mb-4">We really appreciate your donation.
                                Your data will be verified by our medical doctors and, if approved, will be added to our database.
                                If you would like to be recognized as donator or would to discuss further collaboration, please contact
                                <a href="mailto:info@pocovidscrenen.org">info@pocovidscreen.org</a>.</p>
                        </div>
                    </div>
                </div>
                <aside className="thumbs-container justify-content-center mb-4">
                    {results.map((result) => (
                        <div className="thumb" key={result.image.name}>
                            <div className="thumb-inner">
                                <img src={result.preview} alt={`Result for ${result.image.path}`}/>
                            </div>
                        </div>
                    ))}
                </aside>
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <a href="/train" title="Train the AI again" className="button primary round w-100 text-uppercase mt-4 d-block text-center">Donate data again</a>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default TrainResult;
