import React, { useRef, useState } from "react";
import { ISliderBlock } from "./MobileProgressBar";
import "./DesktopProgressBar.pcss"


export const DesktopProgressBar = (props: ISliderBlock) => {
    const [progress, setProgress] = useState('0px')

    const moving = (e: React.MouseEvent<HTMLDivElement>) => {
        console.log(e.nativeEvent.offsetX);

        setProgress(e.nativeEvent.offsetX + 'px')
    }

    const div = useRef()
    console.log(div)

    console.log(500 / props.images.length); //500px width

    return <>
        <div ref={div} className="outside" style={{ width: 'inherit' }} onClick={moving}>
            <div className="inside" style={{ width: progress }}>

            </div>
        </div>
    </>
}
