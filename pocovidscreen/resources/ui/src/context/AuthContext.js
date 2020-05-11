import React, {useState, useEffect, useMemo} from 'react';
import {getToken, setToken} from '../utils/auth';
import {getUser} from '../api/auth';

const AuthContext = React.createContext();

const AuthProvider = ({children}) => {
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
            setCurrentUser
        }
        }> {children}
        </AuthContext.Provider>
    );
}

export {AuthContext, AuthProvider};
