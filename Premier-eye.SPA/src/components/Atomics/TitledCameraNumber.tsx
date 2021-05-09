import Tooltip from '@material-ui/core/Tooltip';
import React from 'react';

const colorForCameras = ['blue', 'tomato', 'orange', 'purple', 'green'];

export default function TitledCameraNumber(props: { cameraId: number }) {
    return (
        <Tooltip title="Номер камеры" aria-label="add">
            <span style={{ color: colorForCameras[props.cameraId] }}> {props.cameraId} </span>
        </Tooltip>
    );
}
