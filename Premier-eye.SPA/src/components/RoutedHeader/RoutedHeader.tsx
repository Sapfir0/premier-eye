import {Route, Switch} from "react-router-dom";
import ButtonAppBar from "./Header";
import Settings from "../pages/Settings";
import React from "react";
import HomePage from "../pages/HomePage";
import { ClientRoutes } from "config/clientRoutes";


export default function () {
    return (<>
            <ButtonAppBar/>
            <Switch>
                <Route path={ClientRoutes.Settings}>
                    <Settings/>
                </Route>
                <Route path={ClientRoutes.Index}>
                    <HomePage/>
                </Route>

            </Switch>
        </>
    )
}
