import React from "react";
import Slider, {ISlider} from "./Slider";
import {myContainer} from "../../config/inversify.config";
import {ISliderPublicAction} from "../../typings/IAction";
import {TYPES} from "../../typings/types";
import {AnyAction, bindActionCreators, Dispatch} from "redux";
import {RootStore} from "../../store";
import {connect} from "react-redux"


type IProps = ISlider

function SliderContainer(props: IProps) {
    return <Slider {...props}/>
}


function mapDispatchToProps(dispatch: Dispatch<AnyAction>) {
    const actions = myContainer.get<ISliderPublicAction>(TYPES.SliderAction)

    return {
        dispatch,
        actions: {
            ...bindActionCreators({
                getImagesFromCamera: actions.getImagesFromCamera,
                getInfoImage: actions.getInfoImage,
                changeCurrentStep: actions.changeCurrentStep,
                changeCurrentCamera: actions.changeCurrentCamera,
            }, dispatch)
        }
    }
}

const authAction = (state: RootStore) => {
    return {
        imageInfo: state.slider.imageInfo,
        imagesList: state.slider.imagesList,
        currentCameraId: state.slider.currentCameraId,
        stepsStore: state.slider.stepsStore,
        stepMap: state.slider.stepMap
    }
}

export default connect(authAction, mapDispatchToProps)(SliderContainer);