import { Card, Grid } from '@material-ui/core';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { observer } from 'mobx-react';
import React, { useEffect } from 'react';
import { MapContainer, TileLayer, useMapEvent } from 'react-leaflet';
import { ObjectColors } from 'typings/sliderTypes';
import { useInject } from '../../services/hooks';
import { TYPES } from '../../typings/types';
import './AreaMap.pcss';
import { AreaMapStore } from './AreaMapStore';
import { CameraListRenderer } from './CameraListRenderer';
import { Legend } from './Legend';
import { ObjectListRenderer } from './ObjectListRenderer';

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

    const colors: ObjectColors = {
        car: 'blue',
        person: 'orange',
    };

    return (
        <Card>
            <h2 style={{ marginLeft: 20 }}> Карта</h2>
            <Grid justify="center" style={{ minHeight: 700 }} container={true}>
                <Grid item={true}>
                    <Legend colors={colors} objects={store.objects} />
                </Grid>
                <Grid style={{ marginLeft: 20 }} item={true}>
                    <MapContainer
                        center={[48.7700865, 44.585401]}
                        zoom={20}
                        scrollWheelZoom={false}
                        className="main-map"
                    >
                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                        <CameraListRenderer cameraList={store.camerasList} />
                        <ObjectListRenderer objects={store.objects} colors={colors} />
                        <LocationMarker />
                    </MapContainer>
                </Grid>
            </Grid>
        </Card>
    );
});
