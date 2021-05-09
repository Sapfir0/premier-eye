import { Divider, ListItem, ListItemText } from '@material-ui/core';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import React from 'react';
import { definitions } from '../../../typings/Dto';
import { detectionsImages } from '../../Atomics/ObjectsImages';
import { ICollapse, ImageInfoStore } from '../ImageInfoStore';
import { ObjectCollapseInfo } from './ObjectCollapseInfo';

export type CollapsableData = ICollapse & definitions['ObjectInfo'];

export interface IObjectInfo {
    element: CollapsableData;
    store: ImageInfoStore<definitions['ObjectInfo']>;
}

export const ObjectInfo = ({ element, store }: IObjectInfo): React.ReactElement => {
    const toggleCollapse = (id: string) => () => {
        store.toggleCollapse(id);
    };
    return (
        <>
            <ListItem button onClick={toggleCollapse(element.id)}>
                <ListItemIcon>{detectionsImages[element.type].icon} </ListItemIcon>
                <ListItemText inset primary={detectionsImages[element.type].title} />
            </ListItem>
            <Divider />
            <ObjectCollapseInfo isOpen={element.open} scores={element.scores} />
        </>
    );
};
