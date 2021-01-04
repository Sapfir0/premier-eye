import React, { useRef, useState, useEffect } from "react";
import { ISliderBlock } from "./MobileProgressBar";
import "./DesktopProgressBar.pcss"


export const DesktopProgressBar = (props: ISliderBlock) => {
    const [progress, setProgress] = useState(props.currentStep + 'px')
    const [playerWidth, setPlayerWidth] = useState(0)

    length = playerWidth / props.images.length

    const marginLeft: number[] = []
    for (let i = 0; i < props.images.length; i++) {
        marginLeft.push(length * (i))
    }


    const moving = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
        const rawOffset = frameIndex * length + e.nativeEvent.offsetX
        const leftOffset = Math.max(...marginLeft.filter((val) => val < rawOffset))

        props.changeCurrentStep(frameIndex)
        setProgress(leftOffset + 'px')
    }

    const onMouseEnter = (frameIndex: number) => (e: React.MouseEvent<HTMLDivElement>) => {
    }

    const ref = useRef(null);
    useEffect(() => {
        setPlayerWidth(ref.current ? ref.current.offsetWidth : 0)
    }, [ref.current]);


    return <>
        <div ref={ref} className="outside" >
            <div className="progress" style={{ width: progress }}></div>
            <div className='pointsContainer'>
                {marginLeft.map((margin, i) => {
                    return <div className="inside" onMouseEnter={onMouseEnter(i)} style={{ width: length }} onClick={moving(i)}>
                       
                    </div>
                })}
            </div>
        </div>
    </>
}
