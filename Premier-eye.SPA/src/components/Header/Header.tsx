import Button from '@material-ui/core/Button';
import React from 'react';
import { NavLink } from 'react-router-dom';
import { ClientRoutes } from '../../config/clientRoutes';
import './Header.pcss';

export const NavButton = (props: { route: string; name: string }) => (
    <Button component={NavLink} to={props.route} activeClassName="selected">
        {props.name}
    </Button>
);

export default function ButtonAppBar() {
    return (
        <div className="header">
            <NavButton route={ClientRoutes.Index} name="Home" />
            <NavButton route={ClientRoutes.AreaMap} name="Map" />
            <NavButton route={ClientRoutes.Logger} name="Logger" />

            <NavButton route={ClientRoutes.Settings} name="Settings" />
        </div>
    );
}
