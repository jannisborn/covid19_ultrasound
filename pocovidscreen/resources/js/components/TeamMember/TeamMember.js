import React from 'react';
import teamMember from './team-member.png'

const TeamMember = (props) => {

    return (
        <div className="team-member text-center">
            <img draggable="false" src={teamMember} className="img-fluid" alt={props.fullName}/>
            <h3>{props.fullName}</h3>
            <p>{props.job}</p>
        </div>
    );
};

export default TeamMember;
