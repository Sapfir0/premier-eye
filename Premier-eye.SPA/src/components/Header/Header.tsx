import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import { Link, Route, Switch } from "react-router-dom";
import SettingsIcon from "@material-ui/icons/Settings";
import React from "react";
import Button from "@material-ui/core/Button"
import { ClientRoutes } from "../../config/clientRoutes";


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
        margin: '0',
        alignItems: "flex-end"
    },
    menuButton: {
        marginRight: theme.spacing(2),
        alignItems: "flex-end"
    },
    title: {
        flexGrow: 1,
        textDecoration: "none",
        color: 'white'
    },
}));

export default function ButtonAppBar() {
    const classes = useStyles();

    return (
        <div className={classes.root}>

            <AppBar position="static">
                <Link to={ClientRoutes.Index}>
                    <Button className={classes.title} >Home</Button>
                </Link>
                <Link to={ClientRoutes.AreaMap}>
                    <Button className={classes.title} >Map</Button>
                </Link>


            </AppBar>

        </div>
    );
}