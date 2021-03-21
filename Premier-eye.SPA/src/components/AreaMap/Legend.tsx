import { Card, List, ListItem, ListItemText } from '@material-ui/core';
import 'leaflet/dist/leaflet.css';
import React from 'react';
import { definitions } from '../../typings/Dto';
import './AreaMap.pcss';

interface LegendProps<T> {
    colors: Map<T, string>;
    objects: definitions['ObjectInfo'][];
}

export function Legend<T extends string>({ colors, objects }: LegendProps<T>): React.ReactElement {
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
                                backgroundColor: colors.get(el.type as T),
                            }}
                        ></div>
                        <ListItemText primary={el.type} />
                    </ListItem>
                ))}
            </List>
        </Card>
    );
}
