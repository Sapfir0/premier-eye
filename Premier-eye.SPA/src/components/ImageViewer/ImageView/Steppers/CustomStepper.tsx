import React from 'react';
import { DesktopProgressBar } from '../../../Atomics/ProgressBar/DesktopProgressBar';
import { BackButton, NextButton } from '../Buttons';
import { IStepper } from './IStepper';

export const CustomStepper = (props: IStepper) => {
    return (
        <>
            <DesktopProgressBar {...props} />
            <div className="controls">
                <BackButton {...props} isDisabled={props.currentStep === 0} />
                <NextButton {...props} isDisabled={props.currentStep === props.images.length - 1} />
            </div>
        </>
    );
};
