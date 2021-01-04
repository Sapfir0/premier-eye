import React from 'react'
import { NextButton, BackButton } from "../Buttons"
import MobileStepper from '@material-ui/core/MobileStepper';
import { ISliderBlock } from "./MobileProgressBar";
import {DesktopProgressBar} from "./DesktopProgressBar"

export class CustomStepper extends React.Component<ISliderBlock> {
    render() {
        return <>
            <DesktopProgressBar {...this.props}/>

        </>
    }
}