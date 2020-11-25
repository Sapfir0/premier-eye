import React from 'react';
import HomePage from "./pages/HomePage"
import ClientRoutes from "../config/clientRoutes";
import ButtonAppBar from "./RoutedHeader/Header";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";


function App() {
    return (
        <Router>
            <ButtonAppBar/>
            <Switch>
                <Route path={ClientRoutes.Index} component={HomePage}/>
            </Switch>
        </Router>
    );
}

export default App;
