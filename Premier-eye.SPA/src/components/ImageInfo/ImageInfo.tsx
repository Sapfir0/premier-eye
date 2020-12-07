import React from "react";
import { Divider, List, ListItem, ListItemText } from "@material-ui/core";
import { withStyles } from '@material-ui/core/styles';
import TitledCameraNumber from "../Atomics/TitledCameraNumber";
import { definitions } from "../../typings/Dto";
import { ICollapse, ImageInfoStore } from "./ImageInfoStore"
import { WarningIfBigDiffBetweenDates } from "../Atomics/Warning/Warning"
import { observer } from "mobx-react";
import { CollapsableData, ObjectInfo } from "./Widgets/ObjectInfo";
import "./ImageInfo.pcss"
import Alert from "@material-ui/lab/Alert";
import { getDiffDay } from "../../services/Time";


interface IImageInfo {
    info: definitions['ImageInfo'],
    store: ImageInfoStore<definitions['ObjectInfo']>
}


@observer
export default class ImageInfo extends React.Component<IImageInfo> {
    constructor(props: IImageInfo) {
        super(props)
    }

    getObjectsUIRepresentation = (data: Array<CollapsableData>) =>
        <List component="nav">
            {data.map((el: CollapsableData) =>
                <ObjectInfo store={this.props.store} key={el.id} element={el} />
            )}
        </List>

    getOldImageWarning = (imageDate: Date) => {
        const diff = getDiffDay(imageDate, new Date())
        
        return <ListItem><Alert severity="error" >{ diff > 1 && <span>Изображений не было уже {diff} дней</span> }</Alert> </ListItem>
    }

    render() {
        const myData = this.props.info

        let objects: JSX.Element | undefined;
        if (myData.objects && myData.objects.length !== 0) {
            if (this.props.store.collapses.length === 0) {
                this.props.store.setCollapses(myData.objects)
            }
            objects = this.getObjectsUIRepresentation(this.props.store.collapses)
        }

        const warningDateDiff = WarningIfBigDiffBetweenDates(new Date(myData.createdAt), new Date(myData.fixationDatetime));


        return (
            <div className="imageInfo">
                <List component="nav" aria-label="main mailbox folders">
                    <ListItem>
                        <TitledCameraNumber cameraId={myData.numberOfCam} />
                    </ListItem>
                    <ListItem> {myData.filename} </ListItem>
                    <ListItem> {myData.fixationDatetime.toString()} {warningDateDiff}</ListItem>
                    
                    {objects}
                    {this.getOldImageWarning(new Date(myData.fixationDatetime))}
                </List>
            </div>
        );
    }
}

