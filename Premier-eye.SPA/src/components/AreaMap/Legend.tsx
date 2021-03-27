import { Card, List, ListItem, ListItemText } from '@material-ui/core';
import 'leaflet/dist/leaflet.css';
import React from 'react';
import { ObjectColors, ObjectTypes } from 'typings/sliderTypes';
import { definitions } from '../../typings/Dto';
import './AreaMap.pcss';

interface LegendProps {
    colors: ObjectColors;
    objects: definitions['ObjectInfo'][];
}

export function Legend({ colors, objects }: LegendProps): React.ReactElement {
    return (
        <Card>
            <List>
                {objects.map((el) => (
                    <ListItem key={el.id}>
                        <div
                            style={{
                                width: 20,
                                height: 10,
                                marginRight: 10,
                                backgroundColor: colors[el.type as ObjectTypes],
                            }}
                        ></div>
                        <ListItemText primary={el.type} />
                    </ListItem>
                ))}
            </List>
        </Card>
    );
}
