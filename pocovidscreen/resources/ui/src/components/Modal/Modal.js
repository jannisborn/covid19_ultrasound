import React from 'react';
import close from './close.svg';

const Modal = ({ handleClose, show, children }) => {
    const showHideClassName = show ? "modal display-block" : "modal display-none";

    return (
        <div className={showHideClassName}>
            <section className="modal-main">
                <div className="modal-content">
                    {children}
                    <button className="close" onClick={handleClose}><img src={close} alt="Close button"/></button>
                </div>
            </section>
        </div>
    );
};

export default Modal;
