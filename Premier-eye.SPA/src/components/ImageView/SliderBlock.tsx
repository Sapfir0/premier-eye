import React from 'react'
import { NextButton, BackButton } from "./Buttons"
import MobileStepper from '@material-ui/core/MobileStepper';
import { definitions } from 'typings/Dto';


export interface IBaseSliderBlock {
    images: Array<definitions['Image']>
    currentStep: number
}

export interface ISliderBlock extends IBaseSliderBlock {
    changeCurrentStep: (step: number) => void
}

export class SlideBlock extends React.Component<ISliderBlock> {
    render() {
        return <>
            <MobileStepper
                steps={this.props.images.length}
                position="static"
                variant="progress"
                activeStep={this.props.currentStep}
                nextButton={<NextButton {...this.props} isDisabled={this.props.currentStep === this.props.images.length - 1} />}
                backButton={<BackButton {...this.props} isDisabled={this.props.currentStep === 0} />}
            />
        </>
    }
}