import React from "react";
import {Divider, ListItem, ListItemText} from "@material-ui/core";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import {detectionsImages} from "../Atomics/ObjectsImages";
import {ObjectCollapseInfo} from "./ObjectCollapseInfo";
import {ICollapse, ImageInfoStore} from "./ImageInfoStore";
import {definitions} from "../../typings/Dto";

export type CollapsableData = ICollapse & definitions['ObjectInfo']

export interface IObjectInfo {
    element: CollapsableData
    store: ImageInfoStore<definitions['ObjectInfo']>
}


export const ObjectInfo = ({element, store}: IObjectInfo) => (
    <>
        <ListItem button onClick={() => store.toggleCollapse(element.id)}>
            <ListItemIcon>{detectionsImages[element.type].icon} </ListItemIcon>
            <ListItemText inset primary={detectionsImages[element.type].title}/>
        </ListItem>
        <Divider/>
        <ObjectCollapseInfo isOpen={element.open} scores={element.scores} />
    </>
)
