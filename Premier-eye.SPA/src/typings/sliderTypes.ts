import {IImageInfo} from "../components/ImageInfo/IImageInfo";
import StepDataStructure from "../services/DataStructure/StepDataStructure";
import {IdPayload} from "./common";

export type ImagesUrlPayload = {
    imagesUrl: string[]
}

export type ChangeStepPayload = {
    cameraId: number
    currentStep: number
}

export type ImagesInfoPayload = {
    imageInfo: IImageInfo
}

export type SrcPayload = {
    src: string
}

export type SliderBasePayload = ImagesInfoPayload & ImagesUrlPayload & SrcPayload & ChangeStepPayload & IdPayload

export type SliderStore = {
    imageInfo: IImageInfo | null
    imagesList: Array<string>
    currentCameraId: number
    stepsStore: StepDataStructure
    stepMap: Map<number, number>
}