import React, { useRef, useState, useEffect } from "react";
import "./DesktopProgressBar.pcss"
import { BackButton, NextButton } from "../../ImageViewer/ImageView/Buttons";
import {range} from "../../../services/utils"
import {IStepper} from "../../ImageViewer/ImageView/Steppers/IStepper";


const toPixels = (num: number) => `${num}px`


export const DesktopProgressBar = (props: IStepper) => {
    const [playerWidth, setPlayerWidth] = useState(600)
    const frameLength = playerWidth / props.images.length

    const ref = useRef<HTMLDivElement>(null);
    useEffect(() => {
        setPlayerWidth( ref.current !== null ? ref.current!.offsetWidth  : 0)
    }, [ref.current]);

    const moving = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
        props.changeCurrentStep(frameIndex)
    }

    const onMouseEnter = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
    }
    
    return <>
        <div ref={ref} className="outside" >
            <div className="progress" style={{width: toPixels(props.currentStep * frameLength)}}/>
            <div className='pointsContainer'>
                {range(props.images.length).map((empty, i) => 
                     <div className="inside" onMouseEnter={onMouseEnter(i)} style={{width: frameLength}} onClick={moving(i)}/>
                )}
            </div>

        </div>
    </>
}
