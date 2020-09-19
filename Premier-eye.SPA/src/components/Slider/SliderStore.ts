import {SliderStore} from "../../typings/sliderTypes";
import StepDataStructure from "../../services/DataStructure/StepDataStructure";


export const sliderStore: SliderStore = {
    imageInfo: null,
    imagesList: [],
    currentCameraId: 1,
    stepsStore: new StepDataStructure(),
    stepMap: new Map<number, number>()
}