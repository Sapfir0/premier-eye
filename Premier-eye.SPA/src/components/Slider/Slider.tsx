import React from 'react';
import ImageView from '../ImageView/ImageView'
import ImageInfo from "../ImageInfo/ImageInfo"
import CamerasList from "../CamerasList/CamerasList"
import {withStyles} from '@material-ui/core/styles';
import {IImageInfo} from "../ImageInfo/IImageInfo";
import {ISliderPublicAction} from "../../typings/IAction";
import "./Slider.pcss"
import StepDataStructure from "../../services/DataStructure/StepDataStructure";

export interface ISlider {

    imagesList: Array<string>,
    imageInfo: IImageInfo | null
    actions: ISliderPublicAction
    currentCameraId: number
    stepMap: Map<number, number>
}


class Slider extends React.Component<ISlider> {

    constructor(props: ISlider) {
        super(props);
    }

    componentDidMount() {
        this.props.actions.getImagesFromCamera(this.props.currentCameraId)
        this.props.actions.changeCurrentStep(this.props.currentCameraId, 0)
    }

    handleCameraChange = (cameraId: number) => {
        this.props.actions.getImagesFromCamera(cameraId)
        this.props.actions.changeCurrentCamera(cameraId)
        const currentStep = this.props.stepMap.get(cameraId) === undefined ? 0 : this.props.stepMap.get(cameraId)
        this.props.actions.changeCurrentStep(cameraId, currentStep!)
    }

    handleCurrentStepChange = (step: number) => {
        this.props.actions.changeCurrentStep(this.props.currentCameraId, step)
    }

    render() {

        return (
            <div className="slider">
                <CamerasList onCameraChange={this.handleCameraChange}/>
                {
                    this.props.imagesList &&
                    <ImageView
                        currentStep={this.props.stepMap.get(this.props.currentCameraId)!}
                        changeCurrentStep={this.handleCurrentStepChange}
                        images={this.props.imagesList}
                        updateStateByInfo={this.props.actions.getInfoImage}
                    />
                }
                {
                    this.props.imageInfo &&
                    <ImageInfo
                        info={this.props.imageInfo}
                    />
                }

            </div>
        );
    }
}


export default Slider;
