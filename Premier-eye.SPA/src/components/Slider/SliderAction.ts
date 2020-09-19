import {injectable} from "inversify";
import {ActionTypePayload, ActionTypePure, ErrorPayload, IdPayload} from "../../typings/common";
import {
    CHANGE_CURRENT_CAMERA,
    CHANGE_CURRENT_STEP,
    GET_IMAGES_FROM_CAMERA, GET_INFO_IMAGE,
    SET_IMAGES_FROM_CAMERA, SET_INFO_IMAGE, SET_SLIDER_ERROR,
    SLIDER_ACTIONS, UNSET_SLIDER_ERROR
} from "../../store/actionNames/sliderActionNames";
import {ChangeStepPayload, ImagesInfoPayload, ImagesUrlPayload, SrcPayload} from "../../typings/sliderTypes";
import {ISliderPrivateAction, ISliderPublicAction} from "../../typings/IAction";
import {IImageInfo} from "../ImageInfo/IImageInfo";
import {BaseInteractionError} from "../../services/Errors/BaseInteractionError";


@injectable()
export default class SliderAction implements ISliderPrivateAction, ISliderPublicAction {

    public changeCurrentCamera = (cameraId: number): ActionTypePayload<IdPayload, SLIDER_ACTIONS> => ({
        type: CHANGE_CURRENT_CAMERA,
        payload: {
            id: cameraId
        }
    })

    public changeCurrentStep = (cameraId: number, currentStep: number): ActionTypePayload<ChangeStepPayload, SLIDER_ACTIONS> => ({
        type: CHANGE_CURRENT_STEP,
        payload: {
            cameraId, currentStep
        }
    })

    public getImagesFromCamera = (cameraId: number): ActionTypePayload<IdPayload, SLIDER_ACTIONS> => ({
        type: GET_IMAGES_FROM_CAMERA,
        payload: {
            id: cameraId
        }
    })

    public setImagesUrlFromCamera = (imagesUrl: string[]): ActionTypePayload<ImagesUrlPayload, SLIDER_ACTIONS> => ({
        type: SET_IMAGES_FROM_CAMERA,
        payload: {
            imagesUrl
        }
    })

    public getInfoImage = (src: string): ActionTypePayload<SrcPayload, SLIDER_ACTIONS> => ({
        type: GET_INFO_IMAGE,
        payload: {
            src
        }
    })

    public setInfoImage = (imageInfo: IImageInfo): ActionTypePayload<ImagesInfoPayload, SLIDER_ACTIONS> => ({
        type: SET_INFO_IMAGE,
        payload: {
            imageInfo
        }
    })

    public setError = (error: BaseInteractionError): ActionTypePayload<ErrorPayload, SLIDER_ACTIONS> => ({
        type: SET_SLIDER_ERROR,
        payload: {
            error
        }
    })

    public unsetError = (): ActionTypePure<SLIDER_ACTIONS> => ({
        type: UNSET_SLIDER_ERROR,
    })

}