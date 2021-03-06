import React from 'react';
import { BrowserRouter as Router, Redirect, Route, Switch } from 'react-router-dom';
import { ClientRoutes } from '../config/clientRoutes';
import './App.pcss';
import ButtonAppBar from './Header/Header';
import AreaMapPage from './pages/AreaMapPage';
import HomePage from './pages/HomePage';
import SettingsPage from './pages/Settings';
import CameraPage from './pages/LoggerPage';

function App() {
    return (
        <Router>
            <ButtonAppBar />
            <Switch>
                <Route path={ClientRoutes.Settings} component={SettingsPage} />
                <Route path={ClientRoutes.AreaMap} component={AreaMapPage} />
                <Route path={ClientRoutes.Logger} component={CameraPage} />
                <Route path={ClientRoutes.Index} component={HomePage} />

                <Redirect to={ClientRoutes.Index} />
            </Switch>
        </Router>
    );
}

export default App;
