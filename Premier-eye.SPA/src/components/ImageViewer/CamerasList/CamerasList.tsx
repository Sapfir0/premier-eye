import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import { definitions } from '../../../typings/Dto';
import "./CamerasList.pcss"
import {BaseCamerasList} from "./BaseCamerasMenu"

interface IProps {
    cameras: definitions['CameraList']
    onCameraChange: (cameraId: string) => void
}

class CamerasList extends React.Component<IProps> {
    constructor(props: IProps) {
        super(props);
    }

    handleListItemClick = (cameraId: string) => () => {
        this.props.onCameraChange(cameraId);
        console.log("Кликнули на камеру ", cameraId);
    }

    render() {
        return (
            <div className="camerasList">
                <List component="nav" aria-label="main mailbox folders">
                    <BaseCamerasList onClick={this.handleListItemClick} cameras={this.props.cameras.items} />
                </List>
            </div>
        );
    }


}

export default CamerasList
