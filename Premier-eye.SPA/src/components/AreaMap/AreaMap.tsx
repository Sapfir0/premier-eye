import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { observer } from 'mobx-react';
import React, { useEffect } from 'react';
import { Circle, MapContainer, Polygon, TileLayer, Tooltip, useMapEvent } from 'react-leaflet';
import { useInject } from '../../services/hooks';
import { TYPES } from '../../typings/types';
import './AreaMap.pcss';
import { AreaMapStore } from './AreaMapStore';

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

    console.log(store.camerasList);
    
    return (
        <>
            Карта
            <MapContainer center={[48.7700865, 44.585401]} zoom={20} scrollWheelZoom={false} className="main-map">
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                {store.camerasList.items.map((camera) => (
                    <React.Fragment key={camera.id}>
                        <Circle pathOptions={{ color: 'red' }} center={camera.latlon} radius={1} />
                        <Polygon pathOptions={{ color: 'green' }} positions={camera.view}>
                            <Tooltip>Камера {camera.id}</Tooltip>
                        </Polygon>
                    </React.Fragment>
                ))}

                {store.objects.map((obj) => (
                    <Circle
                        key={`${obj.latlon.lat}${obj.latlon.lng}`}
                        pathOptions={{ color: 'orange' }}
                        center={obj.latlon}
                        radius={3}
                    >
                        <Tooltip>
                            {obj.type} found on {obj.cameraId}{' '}
                        </Tooltip>
                    </Circle>
                ))}

                <LocationMarker />
            </MapContainer>
        </>
    );
});
