import { Grid } from '@material-ui/core';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { observer } from 'mobx-react';
import React, { useEffect } from 'react';
import { Circle, MapContainer, Polygon, TileLayer, Tooltip, useMapEvent } from 'react-leaflet';
import { useInject } from '../../services/hooks';
import { TYPES } from '../../typings/types';
import './AreaMap.pcss';
import { AreaMapStore } from './AreaMapStore';
import { Legend } from './Legend';

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

function LocationMarker() {
    const map = useMapEvent('click', (e) => {
        console.log(e.latlng);
    });
    return null;
}

export const AreaMap = observer(() => {
    const store = useInject<AreaMapStore>(TYPES.AreaMapStore);
    useEffect(() => {
        store.getCameraList();
        store.getObjectList();
    }, []);
    const cameraPointColor = 'red';
    const cameraViewColor = 'green';
    type keys = 'car' | 'person';

    const colors: Map<keys, string> = new Map([
        ['car', 'blue'],
        ['person', 'orange'],
    ]);

    return (
        <>
            Карта
            <Grid container={true}>
                <Grid item={true}>
                    <Legend colors={colors} objects={store.objects} />
                </Grid>
                <Grid item={true}>
                    <MapContainer
                        center={[48.7700865, 44.585401]}
                        zoom={20}
                        scrollWheelZoom={false}
                        className="main-map"
                    >
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                        {store.camerasList.items.map((camera) => (
                            <React.Fragment key={camera.id}>
                                <Circle pathOptions={{ color: cameraPointColor }} center={camera.latlon} radius={1} />
                                <Polygon
                                    pathOptions={{ color: cameraViewColor }}
                                    opacity={0.5}
                                    positions={[camera.latlon, camera.view[0], camera.view[1]]}
                                >
                                    <Tooltip>Камера {camera.id}</Tooltip>
                                </Polygon>
                                <Polygon pathOptions={{ color: cameraViewColor }} positions={camera.view}>
                                    <Tooltip>Камера {camera.id}</Tooltip>
                                </Polygon>
                            </React.Fragment>
                        ))}

                        {store.objects.map((obj) => (
                            <Circle
                                key={`${obj.latlon.lat}${obj.latlon.lng}`}
                                pathOptions={{ color: colors.get(obj.type as keys) }}
                                center={obj.latlon}
                                radius={3}
                            >
                                <Tooltip>
                                    {obj.type} found on {obj.cameraId}
                                </Tooltip>
                            </Circle>
                        ))}

                        <LocationMarker />
                    </MapContainer>
                </Grid>
            </Grid>
        </>
    );
});
