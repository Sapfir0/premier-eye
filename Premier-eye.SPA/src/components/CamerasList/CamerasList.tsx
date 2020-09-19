import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import {camersCount} from "../../config/app";
import {withStyles} from "@material-ui/core/styles";

const styles = {
    root: {
        width: '100%',
        maxWidth: 360,
    },
};

interface IProps {
    classes: any,
    onCameraChange: (cameraId: number) => void
}

class CamerasList extends React.Component<IProps> {
    constructor(props: IProps) {
        super(props);
    }

    handleListItemClick = (event: any, index: number) => {
        this.props.onCameraChange(index);
        console.log("Кликнули на камеру ", index);
    }

    render() {
        const {classes} = this.props;

        let camerasMenu = [];
        for (let i = 1; i < camersCount + 1; i++) {
            camerasMenu.push(
                <ListItem
                    button key={i}
                    onClick={(event) => this.handleListItemClick(event, i)}
                >
                    Camera {i}
                </ListItem>
            )
        }
        return (
            <div className={classes.root}>
                <List component="nav" aria-label="main mailbox folders">
                    {camerasMenu}
                </List>
            </div>
        );
    }


}

export default  withStyles(styles)(CamerasList)
