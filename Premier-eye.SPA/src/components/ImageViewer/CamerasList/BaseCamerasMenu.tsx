import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import { definitions } from '../../../typings/Dto';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

interface IBaseCamerasMenu {
    cameras: definitions['Camera'][]
    onClick?: (cameraId: string) => () => void
}

export const BaseCamerasList = (props: IBaseCamerasMenu) => (
    <>{props.cameras.map((camera) =>
        <ListItem
            button key={camera.id}
            onClick={props.onClick && props.onClick(camera.id)}
        >
            Camera {camera.id}
        </ListItem>
    )}</>
)


