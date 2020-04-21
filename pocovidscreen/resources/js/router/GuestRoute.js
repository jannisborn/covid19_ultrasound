import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {useAuth} from '../context/AuthContext';

function GuestRoute({component: Component, title, ...rest}) {

    let {authenticated} = useAuth();

    return (
        <Route
            {...rest}
            render={props => authenticated
                ? <Redirect to={{pathname: '/', state: {from: props.location}}}/>
                : <Component {...props} />
            }
        />
    );
};

export default GuestRoute;
