import React, {useContext} from 'react';
import {Route, Redirect} from 'react-router-dom';
import {AuthContext, useAuth} from '../context/AuthContext';

function GuestRoute({component: Component, title, ...rest}) {

    let {authenticated} = useContext(AuthContext);

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
