import { Button, Input } from '@material-ui/core';
import { BaseTable } from '../../components/Base/BaseTable';
import { SliderStore } from '../../components/ImageViewer/Slider/SliderStore';
import { observer } from 'mobx-react';
import React, { useEffect } from 'react';
import { definitions } from 'typings/Dto';
import { useInject } from '../../services/hooks';
import { HeadersBaseSettings } from '../../typings/table';
import { TYPES } from '../../typings/types';
import { BaseTableLayout } from '../Base/BaseTableLayout';
import { SettingsStore } from './SettingsStore';

export const Settings = observer(() => {
    const sliderStore = useInject<SliderStore>(TYPES.SliderStore);
    const settingsStore = useInject<SettingsStore>(TYPES.SettingsStore);

    useEffect(() => {
        sliderStore.getCameraList();
    }, []);

    const addNewCamera = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        settingsStore.addNewCamera({ name: settingsStore.nameOfCamera });
        sliderStore.getCameraList();
    };

    const changeNewCameraName = (event: React.ChangeEvent<HTMLInputElement>) => {
        settingsStore.nameOfCamera = event.target.value;
    };

    const headers: HeadersBaseSettings<definitions['Camera']> = new Map();

    headers.set('name', {
        text: 'Идентификатор камеры',
        convertFunction: (cameraId: string) => `Camera ${cameraId}`,
    });

    headers.set('latlon', {
        text: 'Координаты камеры',
        convertFunction: (latlon: definitions['Camera']['latlon']) =>
            `${latlon.lat.toFixed(5)}; ${latlon.lng.toFixed(5)}`,
    });

    return (
        <>
            <h1>Настройки</h1>
            <Button onClick={settingsStore.startCreatingNewCamera}>Добавить камеру</Button>
            {settingsStore.isCreating && (
                <>
                    <Input onChange={changeNewCameraName} />
                    <Button onClick={addNewCamera}>Добавить</Button>
                    <Button onClick={settingsStore.stopCreatingNewCamera}>Отмена</Button>
                </>
            )}

            <BaseTable<definitions['Camera'], any>
                headers={headers}
                store={settingsStore}
                list={sliderStore.camerasList}
            />
        </>
    );
});
