import React from 'react';
import { myContainer } from '../../config/inversify.config';
import { TYPES } from '../../typings/types';
import { CameraLogger } from '../CameraLogger/CameraLogger';
import { CameraLoggerStore } from '../CameraLogger/CameraLoggerStore';

export default function LoggerPage() {
    return (
        <>
            <CameraLogger />
        </>
    );
}
