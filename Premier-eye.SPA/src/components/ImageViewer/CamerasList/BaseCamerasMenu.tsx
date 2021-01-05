import ListItem from '@material-ui/core/ListItem';
import React from 'react';
import { definitions } from '../../../typings/Dto';

interface IBaseCamerasMenu {
    cameras: definitions['Camera'][];
    onClick?: (cameraId: string) => () => void;
}

export const BaseCamerasList = (props: IBaseCamerasMenu) => (
    <>
        {props.cameras.map((camera) => (
            <ListItem button key={camera.id} onClick={props.onClick && props.onClick(camera.id)}>
                Camera {camera.id}
            </ListItem>
        ))}
    </>
);
