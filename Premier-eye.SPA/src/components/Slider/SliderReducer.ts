import {ISliderReducer} from "../../typings/IReducers";
import {
    ChangeStepPayload,
    ImagesInfoPayload,
    ImagesUrlPayload,
    SliderBasePayload,
    SliderStore,
    SrcPayload
} from "../../typings/sliderTypes";
import {ActionTypePayload, IdPayload} from "../../typings/common";
import {
    CHANGE_CURRENT_CAMERA, CHANGE_CURRENT_STEP,
    SET_IMAGES_FROM_CAMERA,
    SET_INFO_IMAGE,
    SLIDER_ACTIONS
} from "../../store/actionNames/sliderActionNames";
import {sliderStore} from "./SliderStore";
import {injectable} from "inversify";
import {render} from "react-dom";
import {IImageInfo} from "../ImageInfo/IImageInfo";


@injectable()
export default class SliderReducer implements ISliderReducer {
    public getReducer = () => {
        return (state: SliderStore=sliderStore, action: ActionTypePayload<SliderBasePayload, SLIDER_ACTIONS>) =>
            this.reduce(state, action);
    }

    protected setImagesFromCamera(state: SliderStore, payload: ImagesUrlPayload) {
        const newState = {...state}

        newState.imagesList = payload.imagesUrl

        return newState
    }

    protected setInfoAboutImageFromCamera(state: SliderStore, payload: ImagesInfoPayload) {
        const newState = {...state}

        newState.imageInfo = payload.imageInfo

        return newState
    }

    protected setCurrentCamera(state: SliderStore, payload: IdPayload) {
        const newState = {...state}

        newState.currentCameraId = payload.id

        return newState
    }

    protected setCurrentStep(state: SliderStore, payload: ChangeStepPayload) {
        const newState = {...state}

        newState.stepMap = newState.stepsStore.changeStepOnCurrentCamera(payload.cameraId, payload.currentStep)

        return newState
    }

    protected reduce = (state: SliderStore, action: ActionTypePayload<SliderBasePayload, SLIDER_ACTIONS>): SliderStore => {
        switch (action.type) {
            case SET_IMAGES_FROM_CAMERA:
                return this.setImagesFromCamera(state, action.payload)
            case SET_INFO_IMAGE:
                return this.setInfoAboutImageFromCamera(state, action.payload)
            case CHANGE_CURRENT_CAMERA:
                return this.setCurrentCamera(state, action.payload)
            case CHANGE_CURRENT_STEP:
                return this.setCurrentStep(state, action.payload)
            default: {
                return state
            }
        }
    }

}