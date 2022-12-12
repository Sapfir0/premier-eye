import React from 'react';
import { BrowserRouter as Router, Redirect, Route, Switch } from 'react-router-dom';
import { ClientRoutes } from '../config/clientRoutes';
import './App.pcss';
import { AreaMap } from './AreaMap/AreaMap';
import { CameraLogger } from './CameraLogger/CameraLogger';
import ButtonAppBar from './Header/Header';
import { Slider } from './Slider/Slider';
import { Settings } from './Settings/Settings';

function App() {
    return (
        <Router>
            <ButtonAppBar />
            <Switch>
                <Route path={ClientRoutes.Settings} component={Settings} />
                <Route path={ClientRoutes.AreaMap} component={AreaMap} />
                <Route path={ClientRoutes.Logger} component={CameraLogger} />   
                <Route path={ClientRoutes.Index} component={Slider} />
                <Redirect to={ClientRoutes.Index} />
            </Switch>
        </Router>
    );
}

export default App;
