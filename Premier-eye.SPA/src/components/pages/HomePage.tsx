import React from "react";
import Slider from "../ImageViewer/Slider/Slider";
import {myContainer} from "../../config/inversify.config";
import {TYPES} from "../../typings/types";


export default function HomePage() {
    return (
        <>
            <Slider store={myContainer.get(TYPES.SliderStore)}/>
        </>

    )
}



