import {AppContext} from './context/AppContext';
import React, {lazy, Suspense, useContext, useEffect, useRef} from 'react';
import ThemeSwitcher from './components/ThemeSwitcher/ThemeSwitcher'
import Logo from './components/Logo/Logo'
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import {TweenMax, TimelineLite, Power3} from 'gsap';
import {Helmet} from 'react-helmet';
import Button from './components/Button/Button';

const Home = lazy(() => import('./pages/Home/Home'));
const Train = lazy(() => import('./pages/Train/Train'));
const Screen = lazy(() => import('./pages/Screen/Screen'));
const SignIn = lazy(() => import('./pages/Auth/SignIn'));
const SignUp = lazy(() => import('./pages/Auth/SignUp'));
const LoadingMessage = () => `loading...`;

const Layout = () => {
    const context = useContext(AppContext);

    let themeMode = context.themeMode === 'light' ? 'light' : 'dark';
    document.documentElement.className = themeMode;

    let app = useRef(null);
    let headerItems = useRef(null);
    let masterTl = new TimelineLite();

    useEffect(() => {
        TweenMax.to(app, 0, {css: {visibility: 'visible'}});
        if (localStorage.getItem('animated-once') === null) {
            masterTl.from(headerItems.children[0], 1, {opacity: 0, delay: .8, ease: Power3.easeOut}, 'Start master')
                .from(headerItems.children[1], 1, {opacity: 0, delay: .8, ease: Power3.easeOut}, .3)
                .from(headerItems.children[2], 1, {opacity: 0, delay: .8, ease: Power3.easeOut}, .3);

            localStorage.setItem('animated-once', 'true');
        }

    })

    const addChild = (child, position) => {
        masterTl.add(child, position);
    }

    return (
        <div className="app" ref={el => app = el}>
            <Helmet>
                <meta charSet="utf-8" />
                <title>CovidScreen</title>
                <link rel="canonical" href="http://mysite.com/example" />
            </Helmet>
            <header className="app-header py-4 container">
                <div className="row justify-content-between" ref={el => headerItems = el}>
                    <div className="col text-left">
                        <ThemeSwitcher/>
                    </div>
                    <div className="col d-none d-md-block text-center">
                        <Logo/>
                    </div>
                    <div className="col text-right">
                        <Button className="simple mr-3" href="/sign-in" text="Sign in"/>
                        <Button className="round primary" href="/sign-up" text="Sign up"/>
                    </div>
                </div>
            </header>
            <BrowserRouter>
                <main className="app-main">
                    <Switch>
                        <Suspense fallback={<LoadingMessage />}>
                            <Route exact path="/" component={() => <Home timeline={addChild}/>}/>
                            <Route exact path="/train" component={() => <Train timeline={addChild}/>}/>
                            <Route exact path="/screen" component={() => <Screen timeline={addChild}/>}/>
                            <Route exact path="/sign-in" component={() => <SignIn timeline={addChild}/>}/>
                            <Route exact path="/sign-up" component={() => <SignUp timeline={addChild}/>}/>
                        </Suspense>
                        <Route render={() => <h2>404 Page Not Found</h2>} />
                    </Switch>
                </main>
            </BrowserRouter>
        </div>
    )
};

export default Layout;