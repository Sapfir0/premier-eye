import {Route, Switch} from "react-router-dom";
import ButtonAppBar from "./Header";
import Settings from "../pages/Settings";
import React from "react";
import HomePage from "../pages/HomePage";


export default function () {
    return (<>
            <ButtonAppBar/>
            <Switch>
                <Route path="/settings">
                    <Settings/>
                </Route>
                <Route path="/">
                    <HomePage/>
                </Route>

            </Switch>
        </>
    )
}
