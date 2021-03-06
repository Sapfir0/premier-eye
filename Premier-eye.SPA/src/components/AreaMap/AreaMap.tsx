import { observer } from 'mobx-react';
import React from 'react';
import { UploadButton } from '../Atomics/UploadButton/UploadButton';
import { AreaMapStore } from './AreaMapStore';

export interface IAreaMap {
    areaStore: AreaMapStore;
}

@observer
export class AreaMap extends React.Component<IAreaMap> {
    render() {
        return (
            <>
                Карта
                <UploadButton>Добавить карту объекта</UploadButton>
            </>
        );
    }
}
