import React from 'react';
import { myContainer } from '../../config/inversify.config';
import { TYPES } from '../../typings/types';
import { AreaMap } from '../AreaMap/AreaMap';

export default function AreaMapPage() {
    return (
        <>
            <AreaMap areaStore={myContainer.get(TYPES.AreaMapStore)} />
        </>
    );
}
