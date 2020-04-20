import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';
import { useAuth } from '../context/auth';
import useDocumentTitle from '../components/document-title';

function GuestRoute ({ component: Component, title, ...rest }) {
  useDocumentTitle(title);

  let { authenticated } = useAuth();

  return (
    <Route
      {...rest}
      render={props => authenticated
        ? <Redirect to={{ pathname: '/home', state: { from: props.location } }} />
        : <Component {...props} />
      }
    />
  );
};

GuestRoute.displayName = 'Guest Route';

GuestRoute.propTypes = {
  component: PropTypes.func.isRequired,
  rest: PropTypes.object,
  location: PropTypes.object,
  title: PropTypes.string
};

export default GuestRoute;
