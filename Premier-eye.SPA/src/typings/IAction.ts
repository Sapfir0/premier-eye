import {ActionTypePayload, ActionTypePure, ErrorPayload, IdPayload} from "./common";
import {SLIDER_ACTIONS} from "../store/actionNames/sliderActionNames";
import {ChangeStepPayload, ImagesInfoPayload, ImagesUrlPayload, SrcPayload} from "./sliderTypes";
import {IImageInfo} from "../components/ImageInfo/IImageInfo";
import {BaseInteractionError} from "../services/Errors/BaseInteractionError";


export interface ISliderPublicAction {
    getImagesFromCamera: (cameraId: number) => ActionTypePayload<IdPayload, SLIDER_ACTIONS>
    getInfoImage: (src: string) => ActionTypePayload<SrcPayload, SLIDER_ACTIONS>
    changeCurrentStep: (cameraId: number, currentStep: number) => ActionTypePayload<ChangeStepPayload, SLIDER_ACTIONS>
    changeCurrentCamera: (cameraId: number) => ActionTypePayload<IdPayload, SLIDER_ACTIONS>
}


export interface ISliderPrivateAction {
    setImagesUrlFromCamera: (imagesUrl: string[]) => ActionTypePayload<ImagesUrlPayload, SLIDER_ACTIONS>
    setInfoImage: (imageInfo: IImageInfo) => ActionTypePayload<ImagesInfoPayload, SLIDER_ACTIONS>
    unsetError: () => ActionTypePure<SLIDER_ACTIONS>
    setError: (error: BaseInteractionError) => ActionTypePayload<ErrorPayload, SLIDER_ACTIONS>
}