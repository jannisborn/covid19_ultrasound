import React, {useState, useEffect, createContext} from 'react';
import {useMediaPredicate} from "react-media-hook";

const AppContext = createContext();

const AppProvider = props => {
    const preferredTheme = useMediaPredicate('(prefers-color-scheme: dark)') ? 'dark' : 'light';
    const [appData, setApp] = useState({
        themeMode: localStorage.getItem('theme-mode') || preferredTheme,
        changeTheme: mode => setApp(data => (
            {...data, themeMode: mode}
        ))
    })

    useEffect(() => {
        localStorage.setItem('theme-mode', appData.themeMode)
    }, [appData.themeMode])

    return <AppContext.Provider value={appData}>{props.children}</AppContext.Provider>;
};

export {AppContext, AppProvider};