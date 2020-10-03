import React from "react";
import {Popup} from "semantic-ui-react";

const colorForCameras = ['blue', 'red', 'orange', 'purple', 'green']


export default function (props: { cameraId: number }) {
    return(<Popup title="Номер камеры" aria-label="add">
        <span style={{color: colorForCameras[props.cameraId]}}> {props.cameraId} </span>
    </Popup>)

}
