import {TYPES} from "../typings/types";
import {all, takeEvery, throttle} from "redux-saga/effects";
import {myContainer} from "../config/inversify.config";
import SliderSaga from "../components/Slider/SliderSaga";



export default function* rootSaga() {
    const sliderSaga = myContainer.get<SliderSaga>(TYPES.SliderSaga)

    yield all([
        sliderSaga.watch(),
    ])
}
