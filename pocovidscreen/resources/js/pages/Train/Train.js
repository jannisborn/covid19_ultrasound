import React, {useContext, useEffect, useState} from 'react';
import Layout from '../Layout';
import {AppContext} from '../../context/AppContext';
import {useHistory} from 'react-router-dom';
import downloadDark from '../Screen/images/download-dark.svg';
import download from '../Screen/images/download.svg';
import {useDropzone} from 'react-dropzone';
import {Helmet} from 'react-helmet';
import configuration from '../../utils/constants';
import Teaser from '../../components/Teaser/Teaser';

const Train = () => {
    const context = useContext(AppContext);
    const history = useHistory();
    const isLight = context.themeMode === 'light';

    let downloadImage = downloadDark;
    if (isLight) {
        downloadImage = download;
    }

    const [files, setFiles] = useState([]);
    const [label, setLabel] = useState('4');
    useEffect(() => () => {
        files.forEach(file => URL.revokeObjectURL(file.preview));
    }, [files]);

    const {getRootProps, getInputProps, open} = useDropzone({
        accept: 'image/png, image/jpeg, image/jpg, video/mp4, video/mov',
        noClick: true,
        multiple: true,
        noKeyboard: true,
        onDrop: acceptedFiles => {
            setFiles(acceptedFiles.map(file => Object.assign(file, {
                preview: URL.createObjectURL(file)
            })));
        }
    });

    const thumbs = files.map(file => (
        <div className="thumb" key={file.name}>
            <div className="thumb-inner">
                <img src={file.preview}/>
            </div>
        </div>
    ));

    const handleSubmit = (event) => {
        event.preventDefault();
        history.push({
            pathname: '/train/result',
            state: {files: files, label: label}
        })
    };

    const handleLabelChange = (event) => {
        setLabel(event.target.value)
    };

    return (
        <Layout>
            <Helmet>
                <title>Train - {configuration.appTitle}</title>
            </Helmet>
            <Teaser additionalClass="small" teaser="Select the images you want to send to donate data"/>
            <div className="container">
                <form onSubmit={handleSubmit} className="train-form">
                    <div className="row">
                        <div className="col-10 offset-1">
                            <section className="file-upload-area text-center">
                                <img src={downloadImage} className="mt-3 mb-2"/>
                                <div {...getRootProps({className: 'dropzone'})}>
                                    <input {...getInputProps()}/>
                                    <button type="button" className="button primary round my-4 px-5" onClick={open}>
                                        Choose file
                                    </button>
                                    <p>Or drag and drop some files here</p>
                                </div>
                            </section>
                        </div>
                    </div>
                    <aside className="thumbs-container justify-content-center">
                        {thumbs}
                    </aside>
                    <h2 className="text-center with-line">Choose the correct label for your images</h2>
                    <p className="text-center">If you are not sure or you do not know which label to choose, leave it blank.</p>
                    <div className="row">
                        <div className="col-lg-10 offset-lg-1">
                            <div className="train-labels text-center row">
                                <div className="train-label-radio col-4">
                                    <label htmlFor="covid19">
                                        <input type="radio" id="covid19" name="label" value="2" onChange={handleLabelChange}/>
                                        <div className="radio-background"></div>
                                        COVID-19
                                    </label>
                                </div>
                                <div className="train-label-radio col-4">
                                    <label htmlFor="pneumonia">
                                        <input type="radio" id="pneumonia" name="label" value="1" onChange={handleLabelChange}/>
                                        <div className="radio-background"></div>
                                        Pneumonia
                                    </label>
                                </div>
                                <div className="train-label-radio col-4">
                                    <label htmlFor="healthy">
                                        <input type="radio" id="healthy" name="label" value="3" onChange={handleLabelChange}/>
                                        <div className="radio-background"></div>
                                        Healthy
                                    </label>
                                </div>
                            </div>
                            <button disabled={files.length === 0} className="button primary round w-100 text-uppercase mt-4">Confirm</button>
                        </div>
                    </div>
                    <p className="text-center">Do you have a larger dataset or would like to partner with us? Email us at <a href="mailto:info@pocovidscreen.org">mailto:info@pocovidscreen.org</a>, and we will get back to you ASAP.</p>
                </form>
            </div>
            <div className="spacer"></div>
        </Layout>
    );
};

export default Train;
