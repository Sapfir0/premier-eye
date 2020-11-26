import React from 'react';
import ImageView from '../ImageView/ImageView'
import ImageInfo from "../ImageInfo/ImageInfo"
import CamerasList from "../CamerasList/CamerasList"
import "./Slider.pcss"
import { SliderStore } from './SliderStore';
import { observer } from "mobx-react";
import { makeObservable } from "mobx";

export interface ISlider {
    store: SliderStore
}


@observer
class Slider extends React.Component<ISlider> {

    constructor(props: ISlider) {
        super(props);
    }

    async componentDidMount() {
        this.props.store.changeCurrentCamera(1)
        this.props.store.changeCurrentStep(this.props.store.currentCameraId, 0)
        this.props.store.getCameraList()
    }

    handleCameraChange = (cameraId: string) => {
        this.props.store.changeCurrentCamera(cameraId)
        const currentStep = this.props.store.stepMap.get(cameraId) === undefined ? 0 : this.props.store.stepMap.get(cameraId)
        this.props.store.changeCurrentStep(cameraId, currentStep!)
    }

    handleCurrentStepChange = (step: number) => {
        this.props.store.changeCurrentStep(this.props.store.currentCameraId, step)
    }

    render() {
        return (
            <div className="slider">
                <CamerasList
                    cameras={this.props.store.camerasList}
                    onCameraChange={this.handleCameraChange}
                />

                {
                    this.props.store.imagesList &&
                    <ImageView
                        currentStep={this.props.store.stepMap.get(this.props.store.currentCameraId)!}
                        changeCurrentStep={this.handleCurrentStepChange}
                        images={this.props.store.imagesList}
                        updateStateByInfo={this.props.store.getInfoImage}
                    />
                }
                {
                    this.props.store.imageInfo &&
                    <ImageInfo
                        info={this.props.store.imageInfo}
                    />
                }

            </div>
        );
    }
}


export default Slider;
