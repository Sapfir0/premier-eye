import 'leaflet/dist/leaflet.css';
import React from 'react';
import { Circle, Tooltip } from 'react-leaflet';
import { ObjectColors, ObjectTypes } from 'typings/sliderTypes';
import { definitions } from '../../typings/Dto';
import './AreaMap.pcss';

type ObjectListRendererProps = {
    objects: definitions['ObjectInfo'][];
    colors: ObjectColors;
};

export const ObjectListRenderer = ({ objects, colors }: ObjectListRendererProps) => {
    return (
        <>
            {objects.map((obj) => (
                <Circle
                    key={`${obj.latlon.lat}${obj.latlon.lng}`}
                    pathOptions={{ color: colors[obj.type as ObjectTypes] }}
                    center={obj.latlon}
                    radius={3}
                >
                    <Tooltip>
                        {obj.type} found on {obj.cameraId}
                    </Tooltip>
                </Circle>
            ))}
        </>
    );
};
