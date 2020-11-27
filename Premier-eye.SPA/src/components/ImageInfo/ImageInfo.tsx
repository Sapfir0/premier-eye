import React from "react";
import { Collapse, Divider, List, ListItem, ListItemText } from "@material-ui/core";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import { withStyles } from '@material-ui/core/styles';
import TitledCameraNumber from "../Atomics/TitledCameraNumber";
import { definitions } from "../../typings/Dto";
import {ImageInfoStore} from "./ImageInfoStore"
import { detectionsImages } from "../Atomics/ObjectsImages";
import { WarningIfBigDiffBetweenDates } from "../Atomics/Warning/Warning"
import {ObjectCollapseInfo} from "./ObjectCollapseInfo"

const styles = {
    root: {
        marginRight: "15px"
    },
    numberOfCam: {
        display: 'flex',
    },
    error: {
    }
};

interface IProps {
    info: definitions['ImageInfo'],
    classes: any
    store: ImageInfoStore<definitions['ImageInfo']>
}



class ImageInfo extends React.Component<IProps> {
    constructor(props: IProps) {
        super(props)
    }

    getObjectsUIRepresentation = (data: Array<definitions['ObjectInfo']>) => {
        let objects: JSX.Element;
        this.props.store.setCollapses(data.length)

        const parse = (each: definitions['ObjectInfo']) => {
            const element = this.props.store.collapses.find(item => item.id === each.id)

            return <React.Fragment key={each.id}>
                <ListItem button onClick={() => this.props.store.toggleCollapse(each.id)}>
                    <ListItemIcon>{detectionsImages[each.type].icon} </ListItemIcon>
                    <ListItemText inset primary={detectionsImages[each.type].title} />
                </ListItem>
                <Divider />
                {element && <ObjectCollapseInfo isOpen={each.open} scores={each.scores}  />}
            </React.Fragment>
        }


        objects = <List component="nav">
            {data.map((el: definitions['ObjectInfo']) => parse(el))}
        </List>
        return objects

    }


    render() {
        const myData = this.props.info
        const { classes } = this.props;

        let objects: JSX.Element | undefined;
        if (myData.objects) {
            objects = this.getObjectsUIRepresentation(myData.objects)
        }

        const warningDateDiff = WarningIfBigDiffBetweenDates(new Date(myData.createdAt), new Date(myData.fixationDatetime));
        if (myData.numberOfCam < 0) {
            return <div className={classes.error}> Информация с камеры недоступна </div>
        }


        return (
            <div className={classes.root}>
                <List component="nav" aria-label="main mailbox folders">
                    <ListItem>
                        <TitledCameraNumber cameraId={myData.numberOfCam} />
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
