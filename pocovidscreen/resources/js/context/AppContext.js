import React, {useState, useEffect, createContext} from 'react';
import {useMediaPredicate} from "react-media-hook";

const AppContext = createContext();

const AppProvider = ({children}) => {
    const preferredTheme = useMediaPredicate('(prefers-color-scheme: dark)') ? 'dark' : 'light';
    const [appData, setApp] = useState({
        themeMode: localStorage.getItem('theme-mode') || preferredTheme,
        disclaimerAccepted: !!localStorage.getItem('disclaimer-accepted'),
        changeTheme: mode => setApp(data => (
            {...data, themeMode: mode}
        ))
    })

    useEffect(() => {
        localStorage.setItem('theme-mode', appData.themeMode)
    }, [appData.themeMode])

    return <AppContext.Provider value={appData}>{children}</AppContext.Provider>;
};

const acceptDisclaimer = () => {
    localStorage.setItem('disclaimer-accepted', 'true')
};

export {AppContext, AppProvider, acceptDisclaimer};
