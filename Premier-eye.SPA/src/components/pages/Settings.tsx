import { Button, List, Table } from "@material-ui/core";
import { SliderStore } from "../ImageViewer/Slider/SliderStore";
import React from "react";
import { myContainer } from "../../config/inversify.config";
import { TYPES } from "../../typings/types";
import { observer } from "mobx-react";
import { BaseTableLayout } from "../Base/BaseTableLayout"
import {HeadersBaseSettings, HeaderName} from "../../typings/common"

export interface ISettings {
    sliderStore: SliderStore
}

@observer
export class Settings extends React.Component<ISettings> {
    componentDidMount() {
        this.props.sliderStore.getCameraList()
    }

    render() {
        const headers: HeadersBaseSettings<any> = new Map<string, HeaderName<any>>()

        headers.set('id', {text: "Идентификатор камеры", convertFunction: (cameraId: string) => `Camera ${cameraId}`})
        
        return <>
            <h1>Настройки</h1>
            <Button >Добавить камеру</Button>
            <Table>
                <BaseTableLayout headers={headers} list={this.props.sliderStore.camerasList.items} />
            </Table>
        </>

    }
}

export default function SettingsPage() {
    const store = myContainer.get<SliderStore>(TYPES.SliderStore)
    return <Settings sliderStore={store} />
}
