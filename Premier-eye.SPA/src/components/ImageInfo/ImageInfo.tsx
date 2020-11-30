import React from "react";
import {Divider, List, ListItem, ListItemText} from "@material-ui/core";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import {withStyles} from '@material-ui/core/styles';
import TitledCameraNumber from "../Atomics/TitledCameraNumber";
import {definitions} from "../../typings/Dto";
import {ICollapse, ImageInfoStore} from "./ImageInfoStore"
import {detectionsImages} from "../Atomics/ObjectsImages";
import {WarningIfBigDiffBetweenDates} from "../Atomics/Warning/Warning"
import {ObjectCollapseInfo} from "./ObjectCollapseInfo"
import {observer} from "mobx-react";
import {CollapsableData, ObjectInfo} from "./ObjectInfo";

const styles = {
    root: {
        marginRight: "15px"
    },
    numberOfCam: {
        display: 'flex',
    },
    error: {}
};

interface IImageInfo {
    info: definitions['ImageInfo'],
    classes: any
    store: ImageInfoStore<definitions['ObjectInfo']>
}


@observer
class ImageInfo extends React.Component<IImageInfo> {
    constructor(props: IImageInfo) {
        super(props)
    }

    getObjectsUIRepresentation = (data: Array<CollapsableData>) =>
        <List component="nav">
            {data.map((el: CollapsableData) =>
                <ObjectInfo store={this.props.store} key={el.id} element={el}/>
            )}
        </List>


    render() {
        const myData = this.props.info
        const {classes} = this.props;

        let objects: JSX.Element | undefined;
        if (myData.objects && myData.objects.length !== 0) {
            if (this.props.store.collapses.length === 0) {
                this.props.store.setCollapses(myData.objects)
            }
            objects = this.getObjectsUIRepresentation(this.props.store.collapses)
        }

        const warningDateDiff = WarningIfBigDiffBetweenDates(new Date(myData.createdAt), new Date(myData.fixationDatetime));


        return (
            <div className={classes.root}>
                <List component="nav" aria-label="main mailbox folders">
                    <ListItem>
                        <TitledCameraNumber cameraId={myData.numberOfCam}/>
                    </ListItem>
                    <ListItem> {myData.filename} </ListItem>
                    <ListItem> {myData.fixationDatetime.toString()} {warningDateDiff}</ListItem>

                    {objects}
                </List>
            </div>
        );
    }
}

export default withStyles(styles)(ImageInfo)
