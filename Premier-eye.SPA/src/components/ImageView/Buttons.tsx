import React from 'react'
import Button from '@material-ui/core/Button';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';

interface INavigateButton {
    changeCurrentStep: (newStep: number) => void
    isDisabled: boolean
    currentStep: number
}

interface INextButton extends INavigateButton {

}

export const NextButton = (props: INextButton) => {
    const handleNext = () => {
        props.changeCurrentStep(props.currentStep + 1)
    };
    return <Button size="small" onClick={handleNext} disabled={props.isDisabled}>
        Next
    <KeyboardArrowRight />
    </Button>
}

export interface IBackButton extends INavigateButton {

}

export const BackButton = (props: IBackButton) => {
    const handleBack = () => {
        props.changeCurrentStep(props.currentStep - 1)
    };
    return <Button size="small" onClick={handleBack} disabled={props.isDisabled}>
        <KeyboardArrowLeft />
    Back
</Button>
}