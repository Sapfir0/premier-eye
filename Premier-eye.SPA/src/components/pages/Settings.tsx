import { Button, List, Table } from "@material-ui/core";
import { SliderStore } from "../ImageViewer/Slider/SliderStore";
import { BaseCamerasList, BaseCamerasTable } from "../ImageViewer/CamerasList/BaseCamerasMenu";
import React from "react";
import { myContainer } from "../../config/inversify.config";
import { TYPES } from "../../typings/types";
import { observer } from "mobx-react";

export interface ISettings {
    sliderStore: SliderStore
}

@observer
export class Settings extends React.Component<ISettings> {
    componentDidMount() {
        this.props.sliderStore.getCameraList()
    }
    
    render() {
        return <>
            <h1>Настройки</h1>
            <Button >Добавить камеру</Button>
            <Table>
                <BaseCamerasTable cameras={this.props.sliderStore.camerasList.items} />
            </Table>
        </>
    }
   
}

export default function SettingsPage() {
    const store = myContainer.get<SliderStore>(TYPES.SliderStore)
    return <Settings sliderStore={store} />
}
