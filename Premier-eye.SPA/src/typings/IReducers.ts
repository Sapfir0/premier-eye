import {ActionTypePayload} from "./common";
import {SliderBasePayload, SliderStore} from "./sliderTypes";
import {SLIDER_ACTIONS} from "../store/actionNames/sliderActionNames";


export interface ISliderReducer {
    getReducer: () => (state: SliderStore, action: ActionTypePayload<SliderBasePayload, SLIDER_ACTIONS>) => SliderStore

}