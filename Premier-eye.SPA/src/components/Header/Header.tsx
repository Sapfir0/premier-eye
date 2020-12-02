import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import { Link, NavLink, Route, Switch } from "react-router-dom";
import SettingsIcon from "@material-ui/icons/Settings";
import React from "react";
import Button from "@material-ui/core/Button"
import { ClientRoutes } from "../../config/clientRoutes";
import "./Header.pcss"
import { useLocation } from 'react-router-dom'


export const NavButton = (props: {route: string, name: string}) =>
    <Button component={NavLink} to={props.route} activeClassName="selected" >{props.name}</Button>


export default function ButtonAppBar() {
    const location = useLocation();
    console.log(location.pathname);

    return (
        <div className="header">
                <NavButton route={ClientRoutes.Index} name="Home"  />
                <NavButton route={ClientRoutes.AreaMap} name="Map"  />
 
        </div>
    );
}
