import React, {useContext} from 'react';
import {Route, Redirect} from 'react-router-dom';
import {setIntendedUrl} from '../utils/auth';
import {AuthContext, AuthProvider, useAuth} from '../context/AuthContext';

function AuthRoute({component: Component, title, alertMessage, ...rest}) {

    let {authenticated} = useContext(AuthContext);
    return (
        <Route
            {...rest}
            render={props => {
                if (!authenticated) {
                    setIntendedUrl(props.location.pathname);
                }

                return authenticated
                    ? (
                        <Component {...props} />
                    )
                    :
                    <Redirect to={{pathname: '/sign-in', state: {from: props.location, alertMessage: alertMessage}}}/>;
            }
            }
        />
    );
};

export default AuthRoute;
