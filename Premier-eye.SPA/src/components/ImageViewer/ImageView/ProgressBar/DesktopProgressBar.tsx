import React, { useRef, useState, useEffect } from "react";
import { ISliderBlock } from "./MobileProgressBar";
import "./DesktopProgressBar.pcss"
import { BackButton, NextButton } from "../Buttons";
import {range} from "../../../../services/utils"


const toPixels = (num: number) => `${num}px`


export const DesktopProgressBar = (props: ISliderBlock) => {
    const [playerWidth, setPlayerWidth] = useState(600)
    const frameLength = playerWidth / props.images.length

    const ref = useRef(null);
    useEffect(() => {
        setPlayerWidth( ref !== null && ref.current !== null ? ref.current.offsetWidth : 0)
    }, [ref.current]);

    const moving = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
        props.changeCurrentStep(frameIndex)
    }

    const onMouseEnter = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
    }
    
    return <>
        <div ref={ref} className="outside" >
            <div className="progress" style={{ width: toPixels(props.currentStep*frameLength) }}></div>
            <div className='pointsContainer'>
                {range(props.images.length).map((empty, i) => 
                     <div className="inside" onMouseEnter={onMouseEnter(i)} style={{ width: frameLength }} onClick={moving(i)}>
                       
                    </div>
                )}
            </div>

        </div>
    </>
}
