import React from 'react';
import ImageView from '../ImageView/ImageView'
import ImageInfo from "../ImageInfo/ImageInfo"
import CamerasList from "../CamerasList/CamerasList"
import {withStyles} from '@material-ui/core/styles';
import {ISliderPublicAction} from "../../typings/IAction";
import "./Slider.pcss"
import StepDataStructure from "../../services/DataStructure/StepDataStructure";
import {definitions} from "../../typings/Dto";
import { SliderStore } from './SliderStore';

export interface ISlider {
    store: SliderStore
}


class Slider extends React.Component<ISlider> {

    constructor(props: ISlider) {
        super(props);
    }

    componentDidMount() {
        this.props.store.getImagesFromCamera(this.props.store.currentCameraId)
        this.props.store.changeCurrentStep(this.props.store.currentCameraId, 0)
    }

    handleCameraChange = (cameraId: number) => {
        this.props.store.getImagesFromCamera(cameraId)
        this.props.store.changeCurrentCamera(cameraId)
        const currentStep = this.props.store.stepMap.get(cameraId) === undefined ? 0 : this.props.stepMap.get(cameraId)
        this.props.store.changeCurrentStep(cameraId, currentStep!)
    }

    handleCurrentStepChange = (step: number) => {
        this.props.store.changeCurrentStep(this.props.store.currentCameraId, step)
        this.props.store.getInfoImage(this.props.store.imagesList[step])
    }

    render() {
        return (
            <div className="slider">
                <CamerasList onCameraChange={this.handleCameraChange}/>
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
