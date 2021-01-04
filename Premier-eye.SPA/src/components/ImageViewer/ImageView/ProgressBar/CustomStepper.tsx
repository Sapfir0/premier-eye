import React from 'react'
import { NextButton, BackButton } from "../Buttons"
import MobileStepper from '@material-ui/core/MobileStepper';
import { ISliderBlock } from "./MobileProgressBar";
import { DesktopProgressBar } from "./DesktopProgressBar"

export const CustomStepper = (props: ISliderBlock) => {

    return <>
        <DesktopProgressBar {...props} />
        <div className="controls">
            <BackButton {...props} isDisabled={props.currentStep === 0} />

            <NextButton {...props} isDisabled={props.currentStep === props.images.length - 1} />
        </div>
    </>
}
