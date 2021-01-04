import React from 'react';
import ImageView from '../ImageView/ImageView'
import ImageInfo from "../../ImageInfo/ImageInfo"
import CamerasList from "../CamerasList/CamerasList"
import { SliderStore } from './SliderStore';
import { observer } from "mobx-react";
import { myContainer } from '../../../config/inversify.config';
import { TYPES } from '../../../typings/types';
import {ErrorMessageList} from "../../Atomics/ErrorMessage/ErrorMessageList"
import "./Slider.pcss"
import {ChangeDateButton} from "./DataChanger"

export interface ISlider {
    store: SliderStore
}


@observer
export default class Slider extends React.Component<ISlider> {

    constructor(props: ISlider) {
        super(props);
    }

    async componentDidMount() {
        this.props.store.changeCurrentCamera("1")
        this.props.store.changeCurrentStep("1", 0)
        this.props.store.getCameraList()
    }

    handleCameraChange = (cameraId: string) => {
        this.props.store.changeCurrentCamera(cameraId)
        const currentStep = this.props.store.stepMap.get(cameraId) === undefined ? 0 : this.props.store.stepMap.get(cameraId)
        this.props.store.changeCurrentStep(cameraId, currentStep!)
    }

    handleCurrentStepChange = (step: number) => {
        if (this.props.store.camera !== null) {
            this.props.store.changeCurrentStep(this.props.store.camera.id, step)
        }
    }

    render() {
        console.log("reslider")
        return (
            <div className="slider">
                <CamerasList
                    cameras={this.props.store.camerasList}
                    onCameraChange={this.handleCameraChange}
                />

                {
                    this.props.store.camera && this.props.store.camera.images &&
                    <ImageView
                        currentStep={this.props.store.stepMap.get(this.props.store.camera.id)!}
                        changeCurrentStep={this.handleCurrentStepChange}
                        images={this.props.store.camera.images}
                        updateStateByInfo={this.props.store.getInfoImage}
                    />
                }
                {
                    this.props.store.camera && this.props.store.imageInfo &&
                    <ImageInfo
                        cameraOnlineDate={new Date(this.props.store.camera.onlineDate)}
                        store={myContainer.get(TYPES.ImageInfoStore)}
                        info={this.props.store.imageInfo}
                    />
                }
                {
                    this.props.store.errors &&
                    <ErrorMessageList errors={this.props.store.errors} />
                }
            </div>
        );
    }
}

