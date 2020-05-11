import React, {useContext} from 'react';
import {AppContext} from '../../context/AppContext';

const ThemeSwitcher = () => {

    const context = useContext(AppContext);
    const isLight = context.themeMode === 'light';
    const nextThemeMode = isLight ? 'dark' : 'light';

    const handleThemeChange = () => {
        context.changeTheme(nextThemeMode);
    };

    return (
        <div role="button" className="theme-switcher" onClick={handleThemeChange}>
            <div className="theme-switcher-light"></div>
            <div className="theme-switcher-dark"></div>
        </div>
    );
};

export default ThemeSwitcher;
