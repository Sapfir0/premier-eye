import React from 'react'
import { AreaMapStore } from './AreaMapStore'

export interface IAreaMap {
    areaStore: AreaMapStore
}

export class AreaMap extends React.Component<IAreaMap> {
    render() {
        return <> 
            Карта
            
        </>
    }
}