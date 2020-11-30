import React from 'react'
import {NextButton, BackButton} from "./Buttons"
import MobileStepper from '@material-ui/core/MobileStepper';


export interface ISliderBlock {
    images: Array<string>
    changeCurrentStep: (step: number) => void
    currentStep: number
}

export class SlideBlock extends React.Component<ISliderBlock> {
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