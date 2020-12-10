import { Button, Input, List, Table } from "@material-ui/core";
import { SliderStore } from "../ImageViewer/Slider/SliderStore";
import React from "react";
import { myContainer } from "../../config/inversify.config";
import { TYPES } from "../../typings/types";
import { observer } from "mobx-react";
import { BaseTableLayout } from "../Base/BaseTableLayout"
import { HeadersBaseSettings, HeaderName } from "../../typings/common"

export interface ISettings {
    sliderStore: SliderStore

}

@observer
export class Settings extends React.Component<ISettings> {
    componentDidMount() {
        this.props.sliderStore.getCameraList()
    }

    addNewCamera = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        this.props.sliderStore.addNewCamera({name: this.props.sliderStore.nameOfCamera})
    }

    changeNewCameraName = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.props.sliderStore.nameOfCamera = event.target.value
    }


    render() {
        const headers: HeadersBaseSettings<any> = new Map<string | "", HeaderName<any>>()

        headers.set('id', { text: "Идентификатор камеры", convertFunction: (cameraId: string) => `Camera ${cameraId}` })

        return <>
            <h1>Настройки</h1>
            <Button onClick={this.props.sliderStore.startCreatingNewCamera}>Добавить камеру</Button>
            {this.props.sliderStore.isCreating && <>
                <Input onChange={this.changeNewCameraName} />
                <Button onClick={this.addNewCamera}>Добавить</Button>
                <Button onClick={this.props.sliderStore.stopCreatingNewCamera}>Отмена</Button>
            </>}

            <BaseTableLayout<any, any> headers={headers} list={this.props.sliderStore.camerasList.items} />
            
        </>
    }
}
