import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import { Link, Route, Switch } from "react-router-dom";
import SettingsIcon from "@material-ui/icons/Settings";
import React from "react";
import Button from "@material-ui/core/Button"
import { ClientRoutes } from "../../config/clientRoutes";
import "./Header.pcss"


export default function ButtonAppBar() {
    return (
        <div className="header">
                <Link className="title" to={ClientRoutes.Index}>
                    <Button className="title" >Home</Button>
                </Link>
                <Link className="title" to={ClientRoutes.AreaMap}>
                    <Button>Map</Button>
                </Link>
        </div>
    );
}
