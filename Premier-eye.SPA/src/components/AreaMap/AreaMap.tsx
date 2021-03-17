import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { observer } from 'mobx-react';
import React from 'react';
import { Circle, MapContainer, Polygon, TileLayer, useMapEvent } from 'react-leaflet';
import './AreaMap.pcss';
import { AreaMapStore } from './AreaMapStore';

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

export interface IAreaMap {
    areaStore: AreaMapStore;
}

function LocationMarker() {
    const map = useMapEvent('click', (e) => {
        console.log(e.latlng);
    });
    return null;
}



export const AreaMap = observer(() => {
    // for (const firstGeo of camera03) {
    //     for (const secondGeo of camera03) {
    //         console.log(getDistance(firstGeo.lat, firstGeo.lng, secondGeo.lat, secondGeo.lng));
    //     }
    // }
    console.log(getTrapeziumHeight());

    return (
        <>
            Карта
            <MapContainer center={[48.7700865, 44.585401]} zoom={20} scrollWheelZoom={false} className="main-map">
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <Circle pathOptions={{ color: 'purple', fillColor: 'purple' }} center={realCamera07} radius={1} />
                <Polygon pathOptions={{ color: 'purple' }} positions={camera07} />

                <Circle pathOptions={{ color: 'green', fillColor: 'green' }} center={realCamera03} radius={1} />
                <Polygon pathOptions={{ color: 'green' }} positions={camera03} />

                <Circle pathOptions={{ color: 'orange', fillColor: 'orange' }} center={realCamera02} radius={1} />
                <Polygon pathOptions={{ color: 'orange' }} positions={camera02} />
                <Circle pathOptions={{ color: 'red', fillColor: 'red' }} center={realCamera01} radius={1} />
                <Polygon pathOptions={{ color: 'red' }} positions={camera01} />
                <LocationMarker />
            </MapContainer>
        </>
    );
});
