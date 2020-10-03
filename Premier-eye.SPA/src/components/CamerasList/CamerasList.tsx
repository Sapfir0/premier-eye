import React from 'react';
import {camersCount} from "../../config/app";
import {Button, List, ListItem} from "semantic-ui-react";


const styles = {
    root: {
        width: '100%',
        maxWidth: 360,
    },
};

interface IProps {
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

        let camerasMenu = [];
        for (let i = 1; i < camersCount + 1; i++) {
            camerasMenu.push(
                <ListItem
                    button key={i}
                    onClick={(event) => this.handleListItemClick(event, i)}
                >
                    <Button>Camera {i} </Button>
                </ListItem>
            )
        }
        return (
            <div>
                <List component="nav" aria-label="main mailbox folders">
                    {camerasMenu}
                </List>
            </div>
        );
    }


}

export default CamerasList
