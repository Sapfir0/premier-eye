import { Card, Grid } from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';
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
        await this.props.store.getCameraList();
        if (this.props.store.camerasList.items.length > 0) {
            this.props.store.changeCurrentCamera(this.props.store.camerasList.items[0].name);
            this.props.store.changeCurrentStep(this.props.store.camerasList.items[0].name, 0);
        }
    }

    handleCameraChange = async (cameraId: string) => {
        const isCameraExists = this.props.store.camerasList.items.find((camera) => camera.name == cameraId);
        if (isCameraExists !== undefined) {
            await this.props.store.changeCurrentCamera(cameraId);
            const currentStep = this.getCurrentStep(cameraId);
            await this.props.store.changeCurrentStep(cameraId, currentStep);
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
            <Card
                style={{
                    minHeight: 500,
                    // marginTop: 15,
                    // marginLeft: 20,
                    // marginRight: 20,
                }}
            >
                <Grid style={{ marginTop: 5 }} spacing={3} justify="center" container={true}>
                    <Grid item={true}>
                        <CamerasList
                            selectedCameraId={this.props.store.camera?.id ?? '1'}
                            cameras={this.props.store.camerasList}
                            onCameraChange={this.handleCameraChange}
                        />
                    </Grid>
                    <Grid item={true}>
                        {!this.props.store.camera && <Alert severity="warning">No camera found</Alert>}
                        {this.props.store.camera && this.props.store.camera.images && (
                            <ImageView
                                currentStep={this.getCurrentStep(this.props.store.camera.id)}
                                changeCurrentStep={this.handleCurrentStepChange}
                                images={this.props.store.camera.images}
                            />
                        )}
                    </Grid>
                    <Grid item={true}>
                        {this.props.store.camera && this.props.store.imageInfo && (
                            <ImageInfo
                                cameraOnlineDate={new Date(this.props.store.camera.onlineDate)}
                                store={myContainer.get(TYPES.ImageInfoStore)}
                                info={this.props.store.imageInfo}
                            />
                        )}
                    </Grid>
                    <Grid item={true}>
                        {this.props.store.errors && <ErrorMessageList errors={this.props.store.errors} />}
                    </Grid>
                </Grid>
            </Card>
        );
    }
}
