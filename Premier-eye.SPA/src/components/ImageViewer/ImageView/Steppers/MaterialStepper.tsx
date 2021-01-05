import MobileStepper from '@material-ui/core/MobileStepper';
import React from 'react';
import { BackButton, NextButton } from '../Buttons';
import { IStepper } from './IStepper';

export class MaterialStepper extends React.Component<IStepper> {
    render() {
        return (
            <>
                <MobileStepper
                    steps={this.props.images.length}
                    position="static"
                    variant="progress"
                    activeStep={this.props.currentStep}
                    nextButton={
                        <NextButton
                            {...this.props}
                            isDisabled={this.props.currentStep === this.props.images.length - 1}
                        />
                    }
                    backButton={<BackButton {...this.props} isDisabled={this.props.currentStep === 0} />}
                />
            </>
        );
    }
}
