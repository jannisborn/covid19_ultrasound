import React, {useEffect, useState} from 'react';
import Layout from '../Layout';
import Text from '../../components/Content/Text';
import {useLocation} from 'react-router-dom';
import ScreenResult from './ScreenResult';
import gsap from "gsap";

const ScreenResults = () => {

    const location = useLocation();
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let formData = new FormData();
        location.state.files.map((file) => {
            formData.append('image', file);
            fetch('/api/screen', {
                method: 'POST',
                body: formData
            })
            .then(data => data.json())
            .then(data => {
                setLoading(false);
                setResults(results => results.concat({image: file, data: data}));
            })
        });
    }, [location]);

    return (
        <Layout>
            <div className="container spacer-small">
                <Text title="Results"
                      text="We highly recommend to follow approved clinical guidelines for the diagnosis and management of COVID19. By no means you should base your clinical decision solely on the result of this algorithm."/>
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <div className="placeholders" style={{minHeight: location.state.files.length * 400}}>
                            {loading && (<div>Loading...</div>)}
                            {results.map((result, index) => (
                                <ScreenResult key={index} identifier={index} data={result.data} image={result.image}/>
                            ))}
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-lg-10 offset-lg-1">
                        <a href="/screen" title="Run another test" className="button primary round w-100 text-uppercase mt-4 d-block text-center">Run another test</a>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default ScreenResults;
