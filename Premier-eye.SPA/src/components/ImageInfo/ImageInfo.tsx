import React from "react";
import {Collapse, Divider, List, ListItem, ListItemText} from "@material-ui/core";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import {withStyles} from '@material-ui/core/styles';
import TitledWarning from "../atoms/TitledWarning";
import TitledCameraNumber from "../atoms/TitledCameraNumber";
import {ObjectInfo, IImageInfo } from "./IImageInfo";
import {getDiffSecond} from "../../services/Time";
import {getSettings, Settings} from "./SettingsHelper";
import {detectionsImages} from "./ObjectsImages";

const  styles = {
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
    info: IImageInfo,
    classes: any
}

interface IState {
    settings: Array<Settings>
}


class ImageInfo extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props)
        this.state = {settings: getSettings(10)}; // учет максимум 10 объектов на кадре
    }

    handleClick = (id: number) => {
        this.setState(state => ({
            ...state,
            settings: state.settings.map((item: Settings) =>
                item.id === id ? {...item, open: !item.open} : item
            )
        }));
    };

    getObjectsUIRepresentation = (data: Array<ObjectInfo>) => {
        let objects: JSX.Element;

        if (!this.state.settings) {
            this.setState({
                    settings: getSettings(data.length)
                }
            )
        }

        for (let i = 0; i < data.length; i++) { // фиксим объект, нам было бы удобно, чтобы у него был порядковый номер
            data[i].id = i + 1
        }

        const parse = (each: ObjectInfo) => {
            let collapse = {}
            const element = this.state.settings.find(item => item.id === each.id)
            if (element != undefined) {
                collapse = <Collapse
                    in={element.open}
                    timeout="auto"
                    unmountOnExit
                >
                    <List component="div" disablePadding>
                        <ListItem> Степень уверенности: {each.scores * 100}% </ListItem>
                    </List>
                </Collapse>
            }
            return <React.Fragment key={each.id}>
                <ListItem button onClick={() => this.handleClick(each.id)}>
                    <ListItemIcon>{detectionsImages[each.typesOfObject].icon} </ListItemIcon>
                    <ListItemText inset primary={detectionsImages[each.typesOfObject].title}/>
                </ListItem>
                <Divider/>
                {collapse}
            </React.Fragment>
        }

        const red = (pV: Array<JSX.Element>, cV: ObjectInfo) => {
            pV.push(parse(cV));
            return pV;
        }

        objects = <List component="nav">
            {data.reduce(red, [])}
        </List>
        return objects

    }

    warningIfBigDiffBetweenDates = (createdDate: Date, fixationDate: Date, maxDiff = 60 * 60) => {
        const bigDateDiff = getDiffSecond(createdDate, fixationDate) > maxDiff
        let warningDateDiff;
        if (bigDateDiff) {
            const longText = `Запись в базе данных появилась ${createdDate}.`
            warningDateDiff = <TitledWarning text={longText}/>
        }
        return warningDateDiff
    }

    render() {
        const myData = this.props.info
        const {classes} = this.props;

        let objects: JSX.Element | undefined;
        if (myData.objects) {
            objects = this.getObjectsUIRepresentation(myData.objects)
        }

        const warningDateDiff = this.warningIfBigDiffBetweenDates(new Date(myData.createdAt), new Date(myData.fixationDatetime));
        if (myData.numberOfCam < 0) {
            return <div className={classes.error}> Информация с камеры недоступна </div>
        }


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
