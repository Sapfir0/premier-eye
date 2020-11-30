import React from 'react';
import MobileStepper from '@material-ui/core/MobileStepper';
import NotFoundImage from "../Atomics/NotFoundImage";
import "./ImageView.pcss"
import {NextButton, BackButton} from "./Buttons"

interface IImageView {
    images: Array<string>,
    updateStateByInfo: (src: string) => void
    changeCurrentStep: (step: number) => void
    currentStep: number
}


export class SlideBlock extends React.Component<IImageView> {
    render() {
        return <>
            <MobileStepper
                steps={this.props.images.length}
                position="static"
                variant="progress"
                activeStep={this.props.currentStep}
                nextButton={<NextButton {...this.props} isDisabled={this.props.currentStep === 0} />}
                backButton={<BackButton {...this.props} isDisabled={this.props.currentStep === this.props.images.length - 1} />}
            />
        </>
    }
}


export default class ImageView extends React.Component<IImageView> {
    constructor(props: IImageView) {
        super(props);
    }

    public handleStepChange = (step: number) => {
        this.props.changeCurrentStep(step)
    };

    public render() {
        let slideBlock;
        if (this.props.images.hasOwnProperty("error")) {
            slideBlock = <NotFoundImage />
        }
        else {
            slideBlock = <SlideBlock {...this.props} />
        }

        return (
            <div className="imageView">
                {slideBlock}
            </div>
        );
    }
}
