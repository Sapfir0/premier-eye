import { Card, Grid } from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';
import { decrement, flow, increment } from 'fp-ts/function';
import { observer } from 'mobx-react';
import React from 'react';
import { myContainer } from '../../../config/inversify.config';
import { TYPES } from '../../../typings/types';
import { ErrorSnackbar } from '../../Atomics/ErrorSnackbar';
import ImageInfo from '../../ImageInfo/ImageInfo';
import CamerasList from '../CamerasList/CamerasList';
import ImageView from '../ImageView/ImageView';
import './Slider.pcss';
import { SliderStore } from './SliderStore';

export interface ISlider {}

@observer
export default class Slider extends React.Component<ISlider> {
    sliderStore: SliderStore;

    constructor(props: ISlider) {
        super(props);
        this.sliderStore = myContainer.get<SliderStore>(TYPES.SliderStore);
    }

    async componentDidMount() {
        await this.sliderStore.getCameraList();

        const defaultCameraId = this.sliderStore.camerasList[0].name;
        if (this.sliderStore.camerasList.length > 0) {
            await this.sliderStore.changeCurrentCamera(defaultCameraId);
            await this.sliderStore.changeCurrentStep(defaultCameraId, this.getCurrentStep(defaultCameraId));
        }
    }

    handleCameraChange = async (cameraId: string): Promise<void> => {
        const isCameraExists = this.sliderStore.camerasList.find((camera) => camera.name == cameraId);
        if (isCameraExists !== undefined) {
            await this.sliderStore.changeCurrentCamera(cameraId);
            const currentStep = this.getCurrentStep(cameraId);
            await this.sliderStore.changeCurrentStep(cameraId, currentStep);
        }
    };

    handleCurrentStepChange = (step: number): void => {
        if (this.sliderStore.camera !== null && step >= 0 && step < this.sliderStore.camera?.images.length) {
            this.sliderStore.changeCurrentStep(this.sliderStore.camera.id, step);
        }
    };

    getCurrentStep = (cameraId: string): number => {
        const currentStep = this.sliderStore.stepsStore.getCurrentStep(cameraId);
        return currentStep !== undefined ? currentStep : this.sliderStore.camera!.images.length - 1;
    };

    keyPressed = (e: KeyboardEvent): void => {
        const data = new Map();

        data.set('ArrowRight', flow(this.getCurrentStep, increment, this.handleCurrentStepChange));
        data.set('ArrowLeft', flow(this.getCurrentStep, decrement, this.handleCurrentStepChange));
        data.set('ArrowUp', flow(parseInt, decrement, String, this.handleCameraChange)); // Ужас, надо бы поправить и решить что делать с индексами камер
        data.set('ArrowDown', flow(parseInt, increment, String, this.handleCameraChange));

        const action = data.get(e.key);
        if (action) {
            action(this.sliderStore.camera!.id);
        }
    };

    render() {
        document.addEventListener('keydown', this.keyPressed, false);
        const { camera } = this.sliderStore;
        const isCameraAvailable = camera && camera.images.length > 0;

        return (
            <Card
                style={{
                    minHeight: 500,
                }}
            >
                <Grid style={{ marginTop: 5 }} spacing={3} justify="center" container={true}>
                    <Grid item={true}>
                        <CamerasList
                            selectedCameraId={camera?.id ?? '1'}
                            cameras={this.sliderStore.camerasList}
                            onCameraChange={this.handleCameraChange}
                        />
                    </Grid>
                    <Grid item={true}>
                        {!isCameraAvailable && <Alert severity="warning">No camera found</Alert>}
                        {isCameraAvailable && camera && (
                            <ImageView
                                currentStep={this.getCurrentStep(camera.id)}
                                changeCurrentStep={this.handleCurrentStepChange}
                                images={camera.images}
                            />
                        )}
                    </Grid>
                    <Grid item={true}>
                        {camera && isCameraAvailable && this.sliderStore.imageInfo && (
                            <ImageInfo
                                cameraOnlineDate={new Date(camera.onlineDate)}
                                store={myContainer.get(TYPES.ImageInfoStore)}
                                info={this.sliderStore.imageInfo}
                            />
                        )}
                    </Grid>
                    {this.sliderStore.error && <ErrorSnackbar message={this.sliderStore.error.message} />}
                </Grid>
            </Card>
        );
    }
}
