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

const getDistance = (lat1: number, lon1: number, lat2: number, lon2: number) => {
    const R = 6371e3; // metres
    const φ1 = (lat1 * Math.PI) / 180; // φ, λ in radians
    const φ2 = (lat2 * Math.PI) / 180;
    const Δφ = ((lat2 - lat1) * Math.PI) / 180;
    const Δλ = ((lon2 - lon1) * Math.PI) / 180;
    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const d = R * c; // in metres
    return d;
};

// В данном случае всегда первые 2 координаты - это координаты маленького основания, а последние 2 - большого

const camera07 = [
    { lat: 48.77073964423231, lng: 44.585335850715644 },
    { lat: 48.770718430949216, lng: 44.58525538444519 },
    [48.770460335287055, 44.585335850715644],
    [48.7705557954811, 44.58575427532196],
];

const camera03 = [
    { lat: 48.77013859774096, lng: 44.58474040031433 },
    { lat: 48.77009617065794, lng: 44.584847688674934 },
    { lat: 48.77024820087282, lng: 44.585400223731995 },
    { lat: 48.770449728587636, lng: 44.584810137748725 },
];

const camera02 = [
    { lat: 48.770612364399305, lng: 44.58501935005189 },
    { lat: 48.770718430949216, lng: 44.58496034145356 },
    { lat: 48.77096238316364, lng: 44.585287570953376 },
    [48.7705098331881, 44.58536267280579],
];

const camera01 = [
    { lat: 48.7708386394349, lng: 44.58516955375672 },
    { lat: 48.7708598526672, lng: 44.58511590957642 },
    { lat: 48.77098359634368, lon: 44.585325121879585 },
    { lat: 48.770905814639754, lon: 44.58560407161713 },
];

export interface IAreaMap {
    areaStore: AreaMapStore;
}

function LocationMarker() {
    const map = useMapEvent('click', (e) => {
        console.log(e.latlng);
    });
    return null;
}

const realCamera02 = [48.77065479104615, 44.584874510765076];
const realCamera01 = { lat: 48.77081389065253, lon: 44.58502471446992 };
const realCamera03 = [48.77005727913369, 44.58472967147827];
const realCamera07 = [48.770782070771595, 44.5852392911911];

const getTrapeziumHeight = () => {
    const smallBase = getDistance(camera03[0].lat, camera03[0].lng, camera03[1].lat, camera03[1].lng);
    const bigBase = getDistance(camera03[2].lat, camera03[2].lng, camera03[3].lat, camera03[3].lng);
    console.log(smallBase, bigBase);
    console.log(bigBase / smallBase);
    const c = getDistance(camera03[1].lat, camera03[1].lng, camera03[2].lat, camera03[2].lng); // а вот тут можно ошибиться и получить диагонали
    const d = getDistance(camera03[0].lat, camera03[0].lng, camera03[3].lat, camera03[3].lng);

    const dividend = (bigBase - smallBase) ** 2 + c ** 2 - d ** 2;
    const divider = 2 * (bigBase - smallBase);
    const inBigFract = (dividend / divider) ** 2;

    const res = c ** 2 - inBigFract;
    const h = Math.sqrt(res);
    return h;
};

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
