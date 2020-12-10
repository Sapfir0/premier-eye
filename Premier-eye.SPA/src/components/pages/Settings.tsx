import { SliderStore } from "../ImageViewer/Slider/SliderStore";
import React from "react";
import { myContainer } from "../../config/inversify.config";
import {Settings} from "../Settings/Settings"
import { TYPES } from "../../typings/types";


export default function SettingsPage() {
    const store = myContainer.get<SliderStore>(TYPES.SliderStore)
    return <Settings sliderStore={store} />
}
