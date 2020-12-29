import { Button } from '@material-ui/core'
import React from 'react'
import { AreaMapStore } from './AreaMapStore'
import {UploadButton} from "../Atomics/UploadButton/UploadButton"
import {observer} from "mobx-react"

export interface IAreaMap {
    areaStore: AreaMapStore
}

@observer
export class AreaMap extends React.Component<IAreaMap> {
    render() {
        return <> 
            Карта
            <UploadButton onClick={this.props.areaStore.addNewCard}>Добавить карту объекта</UploadButton>

        </>
    }
}