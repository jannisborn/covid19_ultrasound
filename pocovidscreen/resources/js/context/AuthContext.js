import React, { useState, useEffect, useMemo} from 'react';
import PropTypes from 'prop-types';
import { getToken, setToken } from '../utils/auth';
import {getUser} from '../api/auth';

const AuthContext = React.createContext();

AuthProvider.propTypes = {
  children: PropTypes.element.isRequired
};

function AuthProvider ({ children }) {
  const [initializing, setInitializing] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);
  const authenticated = useMemo(() => !!currentUser, [currentUser]);

  const initAuth = () => {
    return getToken()
      ? getUser()
      : Promise.resolve(null);
  };

  useEffect(() => {
    initAuth().then((user) => {
      setInitializing(false);
      setCurrentUser(user);
    });
  }, []);

  return (
    <AuthContext.Provider value={{
      initializing,
      authenticated,
      currentUser,
      setToken,
      setCurrentUser }
    }> { children }
    </AuthContext.Provider>
  );
}

function useAuth () {
  const context = React.useContext(AuthContext);

  if (context === undefined) {
    throw new Error(`useAuth must be used within a AuthProvider`);
  }

  return context;
}

export { AuthProvider, useAuth };
