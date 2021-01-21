import React from 'react';
import Footer from '../components/Footer/Footer';

const Train = ({className, ...props}) => {
    return (
        <>
            <main className="app-main">
                <div className={className}>
                    {props.children}
                </div>
            </main>
            <Footer/>
        </>
    );
};

export default Train;
