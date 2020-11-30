import React from 'react';
import HomePage from "./pages/HomePage"
import {ClientRoutes} from "../config/clientRoutes";
import ButtonAppBar from "./Header/Header";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
import Settings from './pages/Settings';
import { AreaMap } from './AreaMap/AreaMap';
import "./App.pcss"


function App() {
    return (
        <Router>
            <ButtonAppBar/>
            <Switch>
                <Route path={ClientRoutes.Index} component={HomePage}/>
                <Route path={ClientRoutes.Settings} component={Settings} />
                <Route path={ClientRoutes.AreaMap} component={AreaMap} />
            </Switch>
        </Router>
    );
}

export default App;
