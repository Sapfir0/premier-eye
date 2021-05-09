import { List, ListItem } from '@material-ui/core';
import VideocamIcon from '@material-ui/icons/Videocam';
import Alert from '@material-ui/lab/Alert';
import { observer } from 'mobx-react';
import React from 'react';
import { getDiffDay } from '../../services/Time';
import { definitions } from '../../typings/Dto';
import TitledCameraNumber from '../Atomics/TitledCameraNumber';
import { WarningIfBigDiffBetweenDates } from '../Atomics/Warning/Warning';
import './ImageInfo.pcss';
import { ImageInfoStore } from './ImageInfoStore';
import { CollapsableData, ObjectInfo } from './Widgets/ObjectInfo';

interface IImageInfo {
    info: definitions['ImageInfo'];
    store: ImageInfoStore<definitions['ObjectInfo']>;
    cameraOnlineDate: Date;
}

@observer
export default class ImageInfo extends React.Component<IImageInfo> {
    constructor(props: IImageInfo) {
        super(props);
    }

    getObjectsUIRepresentation = (data: Array<CollapsableData>) => (
        <List component="nav">
            {data.map((el: CollapsableData) => (
                <ObjectInfo store={this.props.store} key={el.id} element={el} />
            ))}
        </List>
    );

    getOldImageWarning = (imageDate: Date) => {
        const diff = getDiffDay(imageDate, new Date());

        if (diff > 1) {
            return (
                <ListItem>
                    <Alert severity="warning">
                        <span>Изображений не было уже {diff} дней</span>
                    </Alert>
                </ListItem>
            );
        }
    };

    render() {
        const { objects, createdAt, fixationDatetime, filename, numberOfCam } = this.props.info;

        if (objects && objects.length !== 0) {
            if (this.props.store.collapses.length === 0) {
                this.props.store.setCollapses(objects);
            }
        }

        const warningDateDiff = WarningIfBigDiffBetweenDates(new Date(createdAt), new Date(fixationDatetime));

        return (
            <div className="imageInfo">
                <List component="nav" aria-label="main mailbox folders">
                    <ListItem>
                        <VideocamIcon />
                        <TitledCameraNumber cameraId={numberOfCam} />
                    </ListItem>
                    <ListItem> {filename} </ListItem>
                    <ListItem>
                        {new Date(fixationDatetime).toLocaleString('ru', { timeZone: 'UTC' })}
                        {warningDateDiff}
                    </ListItem>

                    {this.getObjectsUIRepresentation(this.props.store.collapses)}
                    {this.getOldImageWarning(this.props.cameraOnlineDate)}
                </List>
            </div>
        );
    }
}
