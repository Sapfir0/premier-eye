import { List, ListItem } from '@material-ui/core';
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
                    <Alert severity="error">
                        <span>Изображений не было уже {diff} дней</span>
                    </Alert>
                </ListItem>
            );
        }
    };

    render() {
        const myData = this.props.info;

        let objects: JSX.Element | undefined;
        if (myData.objects && myData.objects.length !== 0) {
            if (this.props.store.collapses.length === 0) {
                this.props.store.setCollapses(myData.objects);
            }
            objects = this.getObjectsUIRepresentation(this.props.store.collapses);
        }

        const warningDateDiff = WarningIfBigDiffBetweenDates(
            new Date(myData.createdAt),
            new Date(myData.fixationDatetime),
        );

        return (
            <div className="imageInfo">
                <List component="nav" aria-label="main mailbox folders">
                    <ListItem>
                        <TitledCameraNumber cameraId={myData.numberOfCam} />
                    </ListItem>
                    <ListItem> {myData.filename} </ListItem>
                    <ListItem>
                        {new Date(myData.fixationDatetime).toLocaleDateString()} {warningDateDiff}
                    </ListItem>

                    {objects}
                    {this.getOldImageWarning(this.props.cameraOnlineDate)}
                </List>
            </div>
        );
    }
}
