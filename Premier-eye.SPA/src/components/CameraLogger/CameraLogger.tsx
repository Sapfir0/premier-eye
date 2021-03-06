import { Paper } from '@material-ui/core';
// import { Map } from 'immutable';
import { observer } from 'mobx-react';
import React, { MouseEventHandler, useEffect } from 'react';
import { definitions } from 'typings/Dto';
import { HeadersBaseSettings, SortDirection } from 'typings/table';
import { BaseTable } from '../../components/Base/BaseTable';
import { SortButton } from '../Atomics/SortButton';
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

    headers.set('timestamp', {
        text: 'Дата',
        convertFunction: (date: string) => {
            return new Date(date).toLocaleString('ru', { timeZone: 'UTC' });
        },
        buttons: {
            sortButton: {
                element: (onClick: MouseEventHandler, selected: boolean, direction: SortDirection) => (
                    <SortButton onClick={onClick} selected={selected} direction={direction} />
                ),
                active: false,
                callback: (name, direction) => {
                    console.log(name, direction);
                },
                sortDirection: 'asc',
            },
        },
    });
    headers.set('title', { text: 'Описание' });

    return (
        <Paper>
            <BaseTable<definitions['DTOLog'], any> headers={headers} list={props.cameraLoggerStore.events} />
        </Paper>
    );
});
