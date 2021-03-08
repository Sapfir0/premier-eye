import { IconButton, Paper } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
// import { Map } from 'immutable';
import { observer } from 'mobx-react';
import React, { useEffect } from 'react';
import { HeadersBaseSettings } from 'typings/table';
import { BaseTable } from '../../components/Base/BaseTable';
import { useInject } from '../../services/hooks';
import { definitions } from '../../typings/Dto';
import { TYPES } from '../../typings/types';
import { CameraLoggerStore } from './CameraLoggerStore';

export interface CameraLoggerProps {}

export const CameraLogger = observer((props: CameraLoggerProps) => {
    const cameraLoggerStore = useInject<CameraLoggerStore>(TYPES.CameraLoggerStore);

    useEffect(() => {
        cameraLoggerStore.getLogs();
    }, []);

    const headers: HeadersBaseSettings<definitions['DTOLog']> = new Map();
    headers.set('cameraId', { text: 'Камера' });

    headers.set('timestamp', {
        text: 'Дата',
        convertFunction: (date: string) => {
            return new Date(date).toLocaleString('ru', { timeZone: 'UTC' });
        },
        buttons: {
            filterButton: {
                input: (onChange: (event: React.ChangeEvent<HTMLInputElement>) => void, onClose: () => void) => {
                    return (
                        <>
                            <input className="table-action" onChange={onChange} type="date"></input>{' '}
                            <IconButton onClick={onClose}>
                                <CloseIcon />
                            </IconButton>
                        </>
                    );
                },
            },
        },
    });
    headers.set('title', { text: 'Описание' });

    return (
        <Paper>
            <BaseTable<definitions['DTOLog'], any>
                store={cameraLoggerStore}
                headers={headers}
                list={cameraLoggerStore.events}
            />
        </Paper>
    );
});
