import React from 'react';
import HomePage from "./pages/HomePage"
import {ClientRoutes} from "../config/clientRoutes";
import ButtonAppBar from "./Header/Header";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
} from "react-router-dom";
import SettingsPage from './pages/Settings';
import { AreaMap } from './AreaMap/AreaMap';
import "./App.pcss"


function App() {
    return (
        <Router>
            <ButtonAppBar/>
            <Switch>
                <Route path={ClientRoutes.Settings} component={SettingsPage} />
                <Route path={ClientRoutes.AreaMap} component={AreaMap} />

                <Route path={ClientRoutes.Index} component={HomePage}/>

                <Redirect to={ClientRoutes.Index} />
            </Switch>
        </Router>
    );
}

export default App;
