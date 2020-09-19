import React from 'react';
import HomePage from "./pages/HomePage"

import {ConnectedRouter} from "connected-react-router";
import {Route, Switch} from "react-router-dom"
import ClientRoutes from "../config/clientRoutes";
import ButtonAppBar from "./RoutedHeader/Header";
import {myContainer} from "../config/inversify.config";
import {IUrlService} from "../services/typings/IUrlService";
import {TYPES} from "../typings/types";
import UrlService from "../services/UrlService";

const router = myContainer.get<UrlService>(TYPES.UrlService)



function App() {
    return (
        <ConnectedRouter history={router.history}>
            <ButtonAppBar />
            <Switch>
                <Route path={ClientRoutes.Index} component={HomePage} />
            </Switch>

        </ConnectedRouter>
    );
}

export default App;
