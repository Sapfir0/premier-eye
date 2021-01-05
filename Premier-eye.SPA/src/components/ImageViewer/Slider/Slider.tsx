import { decrement, flow, increment } from 'fp-ts/function';
import { observer } from 'mobx-react';
import React from 'react';
import { myContainer } from '../../../config/inversify.config';
import { TYPES } from '../../../typings/types';
import { ErrorMessageList } from '../../Atomics/ErrorMessage/ErrorMessageList';
import ImageInfo from '../../ImageInfo/ImageInfo';
import CamerasList from '../CamerasList/CamerasList';
import ImageView from '../ImageView/ImageView';
import './Slider.pcss';
import { SliderStore } from './SliderStore';

export interface ISlider {
    store: SliderStore;
}

@observer
export default class Slider extends React.Component<ISlider> {
    constructor(props: ISlider) {
        super(props);
    }

    async componentDidMount() {
        this.props.store.changeCurrentCamera('1');
        this.props.store.changeCurrentStep('1', 0);
        this.props.store.getCameraList();
    }

    handleCameraChange = (cameraId: string) => {
        const isCameraExists = this.props.store.camerasList.items.find((camera) => camera.id == cameraId);
        if (isCameraExists !== undefined) {
            this.props.store.changeCurrentCamera(cameraId);
            const currentStep = this.getCurrentStep(cameraId);
            this.props.store.changeCurrentStep(cameraId, currentStep);
        }
    };

    handleCurrentStepChange = (step: number) => {
        if (this.props.store.camera !== null && step >= 0 && step < this.props.store.camera?.images.length) {
            this.props.store.changeCurrentStep(this.props.store.camera.id, step);
        }
    };

    getCurrentStep = (cameraId: string) => {
        return this.props.store.stepsStore.getCurrentStep(cameraId);
    };

    keyPressed = (e: KeyboardEvent) => {
        const data = new Map();

        data.set('ArrowRight', flow(this.getCurrentStep, increment, this.handleCurrentStepChange));
        data.set('ArrowLeft', flow(this.getCurrentStep, decrement, this.handleCurrentStepChange));
        data.set('ArrowUp', flow(parseInt, decrement, String, this.handleCameraChange)); // Ужас, надо бы поправить и решить что делать с индексами камер
        data.set('ArrowDown', flow(parseInt, increment, String, this.handleCameraChange));

        const action = data.get(e.key);
        if (action) {
            action(this.props.store.camera!.id);
        }
    };

    render() {
        // console.log("reslider")
        document.addEventListener('keydown', this.keyPressed, false);
        return (
            <div className="slider">
                <CamerasList cameras={this.props.store.camerasList} onCameraChange={this.handleCameraChange} />
                {this.props.store.camera && this.props.store.camera.images && (
                    <ImageView
                        currentStep={this.getCurrentStep(this.props.store.camera.id)}
                        changeCurrentStep={this.handleCurrentStepChange}
                        images={this.props.store.camera.images}
                        updateStateByInfo={this.props.store.getInfoImage}
                    />
                )}
                {this.props.store.camera && this.props.store.imageInfo && (
                    <ImageInfo
                        cameraOnlineDate={new Date(this.props.store.camera.onlineDate)}
                        store={myContainer.get(TYPES.ImageInfoStore)}
                        info={this.props.store.imageInfo}
                    />
                )}
                {this.props.store.errors && <ErrorMessageList errors={this.props.store.errors} />}
            </div>
        );
    }
}
