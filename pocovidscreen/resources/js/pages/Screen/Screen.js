import React, {useContext, useEffect, useState} from 'react';
import Teaser from '../../components/Teaser/Teaser';
import {Helmet} from 'react-helmet';
import configuration from '../../utils/constants';
import {useDropzone} from 'react-dropzone';
import Layout from '../Layout';
import download from './images/download.svg';
import downloadDark from './images/download-dark.svg';
import {AppContext} from '../../context/AppContext';
import {useHistory} from 'react-router-dom';

const Screen = () => {

    const context = useContext(AppContext);
    const history = useHistory();
    const isLight = context.themeMode === 'light';

    let downloadImage = downloadDark;
    if (isLight) {
        downloadImage = download;
    }

    const thumbsContainer = {
        display: 'flex',
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginTop: 16
    };

    const thumb = {
        display: 'inline-flex',
        borderRadius: 7,
        marginBottom: 8,
        marginRight: 8,
        width: 150,
        height: 150,
        padding: 0,
        overflow: 'hidden',
        boxSizing: 'border-box'
    };

    const thumbInner = {
        display: 'flex',
        minWidth: 0,
        overflow: 'hidden'
    };

    const img = {
        display: 'block',
        width: 'auto',
        height: '100%'
    };

    const [files, setFiles] = useState([]);

    useEffect(() => () => {
        files.forEach(file => URL.revokeObjectURL(file.preview));
    }, [files]);

    const {getRootProps, getInputProps, open} = useDropzone({
        accept: 'image/png, image/jpeg, image/jpg',
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
        <div style={thumb} key={file.name}>
            <div style={thumbInner}>
                <img src={file.preview} style={img}/>
            </div>
        </div>
    ));

    const handleSubmit = (event) => {
        event.preventDefault();
        history.push({
            pathname: '/screen/results',
            state: {files: files}
        })
    };

    return (
        <Layout>
            <Helmet>
                <title>Screen - {configuration.appTitle}</title>
            </Helmet>
            <Teaser additionalClass="small" teaser="Select the images you want to analyses"/>
            <div className="container">
                <form onSubmit={handleSubmit}>
                    <div className="row">
                        <div className="col-lg-10 offset-lg-1">
                            <section className="custom-dropzone text-center">
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
                    <aside className="justify-content-center" style={thumbsContainer}>
                        {thumbs}
                    </aside>
                    <div className="row">
                        <div className="col-lg-10 offset-lg-1">
                            <button className="button primary round w-100 text-uppercase mt-4">Confirm</button>
                        </div>
                    </div>
                </form>
            </div>
            <div className="spacer"></div>
        </Layout>
    );
};

export default Screen;
