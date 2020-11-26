import {Route, Switch} from "react-router-dom";
import ButtonAppBar from "./Header";
import Settings from "../pages/Settings";
import React from "react";
import HomePage from "../pages/HomePage";
import { ClientRoutes } from "config/clientRoutes";
import { AreaMap } from "../AreaMap/AreaMap";


export default function () {
    return (<>
            <ButtonAppBar/>
            <Switch>
                <Route path={ClientRoutes.Settings} component={Settings} />
                <Route path={ClientRoutes.Index} component={HomePage} />
                <Route path={ClientRoutes.AreaMap} component={AreaMap} />
            </Switch>
        </>
    )
}
