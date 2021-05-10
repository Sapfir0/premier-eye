import ListItem from '@material-ui/core/ListItem';
import React from 'react';
import { definitions } from '../../typings/Dto';

interface IBaseCamerasMenu {
    cameras: definitions['Camera'][];
    onClick?: (cameraId: string) => () => void;
    selectedId: string;
}

export const BaseCamerasList = (props: IBaseCamerasMenu) => (
    <>
        {props.cameras.map((camera) => (
            <ListItem
                selected={props.selectedId == camera.name}
                button
                key={camera.id}
                onClick={props.onClick && props.onClick(camera.name)}
            >
                Camera {camera.name}
            </ListItem>
        ))}
    </>
);
