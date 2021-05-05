import 'leaflet/dist/leaflet.css';
import React from 'react';
import { Circle, Polygon, Tooltip } from 'react-leaflet';
import { definitions } from '../../typings/Dto';
import './AreaMap.pcss';

export const CameraListRenderer = ({ cameraList }: { cameraList: definitions['CameraList']['items'] }) => {
    const cameraPointColor = 'red';
    const cameraViewColor = 'green';

    return (
        <>
            {cameraList.map((camera) => (
                <React.Fragment key={camera.id}>
                    <Circle pathOptions={{ color: cameraPointColor }} center={camera.coordinates} radius={1} />
                    <Polygon
                        pathOptions={{ color: cameraViewColor }}
                        opacity={0.5}
                        positions={[camera.coordinates, camera.view[0], camera.view[1]]}
                    >
                        <Tooltip>Камера {camera.id}</Tooltip>
                    </Polygon>
                    <Polygon pathOptions={{ color: cameraViewColor }} positions={camera.view}>
                        <Tooltip>Камера {camera.id}</Tooltip>
                    </Polygon>
                </React.Fragment>
            ))}
        </>
    );
};
