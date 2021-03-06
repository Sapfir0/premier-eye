import { Paper } from '@material-ui/core';
// import { Map } from 'immutable';
import { observer } from 'mobx-react';
import React, { useEffect } from 'react';
import { HeadersBaseSettings } from 'typings/common';
import { definitions } from 'typings/Dto';
import { BaseTableLayout } from '../../components/Base/BaseTableLayout';
import { CameraLoggerStore } from './CameraLoggerStore';

export interface CameraLoggerProps {
    cameraLoggerStore: CameraLoggerStore;
}

export const CameraLogger = observer((props: CameraLoggerProps) => {
    useEffect(() => {
        props.cameraLoggerStore.getLogs();
    }, []);

    const headers: HeadersBaseSettings<definitions['DTOLog']> = new Map();
    headers.set('cameraId', { text: 'Камера' });
    headers.set('timestamp', { text: 'Дата' });
    headers.set('title', { text: 'Описание' });

    return (
        <Paper>
            <BaseTableLayout<definitions['DTOLog'], any> headers={headers} list={props.cameraLoggerStore.events} />
        </Paper>
    );
});
