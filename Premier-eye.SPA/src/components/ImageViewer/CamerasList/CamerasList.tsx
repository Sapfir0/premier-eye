import List from '@material-ui/core/List';
import React from 'react';
import { definitions } from '../../../typings/Dto';
import { BaseCamerasList } from './BaseCamerasMenu';
import './CamerasList.pcss';

interface IProps {
    cameras: definitions['CameraList'];
    onCameraChange: (cameraId: string) => void;
    selectedCameraId: string;
}

class CamerasList extends React.Component<IProps> {
    constructor(props: IProps) {
        super(props);
    }

    handleListItemClick = (cameraId: string) => () => {
        this.props.onCameraChange(cameraId);
        // console.log("Кликнули на камеру ", cameraId);
    };

    render() {
        return (
            <div className="camerasList">
                <List component="nav" aria-label="main mailbox folders">
                    <BaseCamerasList
                        selectedId={this.props.selectedCameraId}
                        onClick={this.handleListItemClick}
                        cameras={this.props.cameras.items}
                    />
                </List>
            </div>
        );
    }
}

export default CamerasList;
