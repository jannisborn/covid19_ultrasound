import React from 'react';

const TeamMember = (props) => {

    return (
        <div className="team-member text-center">
            <img draggable="false" src={props.image} className="img-fluid" alt={props.fullName}/>
            <h3>{props.fullName}</h3>
            <p>{props.job}</p>
        </div>
    );
};

export default TeamMember;
