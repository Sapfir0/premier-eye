import {Link, Route, Switch} from "react-router-dom";
import React from "react";
import Settings from "../pages/Settings";
import HomePage from "../pages/HomePage";
import ClientRoutes from "../../config/clientRoutes";
import {Button} from "semantic-ui-react";




// const useStyles = prefixer({
//     root: {
//         flexGrow: 1,
//         alignItems: "flex-end"
//     },
//     menuButton: {
//         marginRight: theme.spacing(2),
//         alignItems: "flex-end"
//     },
//     title: {
//         flexGrow: 1,
//         textDecoration: "none",
//         color: 'white'
//     },
// })

export default function ButtonAppBar() {
    // const classes = useStyles();

    return (
        <div>


            <Link to={ClientRoutes.Index}>
                <Button>
                    Home
                </Button>
            </Link>


        </div>
    );
}
