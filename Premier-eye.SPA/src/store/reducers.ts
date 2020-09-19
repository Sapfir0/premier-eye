import {combineReducers, ReducersMapObject} from 'redux';
import {connectRouter} from "connected-react-router";
import {History} from "history";
import {TYPES} from "../typings/types";
import {myContainer} from "../config/inversify.config";
import SliderReducer from "../components/Slider/SliderReducer";

const sliderReducer = myContainer.get<SliderReducer>(TYPES.SliderReducer)


const createRootReducer = (history: History) => combineReducers({
    router: connectRouter(history),
    slider: sliderReducer.getReducer()

});


export default createRootReducer
