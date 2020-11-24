import {ActionTypePayload} from "./common";
import {SliderBasePayload, ISliderStore} from "./sliderTypes";
import {SLIDER_ACTIONS} from "../store/actionNames/sliderActionNames";


export interface ISliderReducer {
    getReducer: () => (state: ISliderStore, action: ActionTypePayload<SliderBasePayload, SLIDER_ACTIONS>) => ISliderStore

}