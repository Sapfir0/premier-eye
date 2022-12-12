import { Card, Grid } from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';
import { decrement, flow, increment } from 'fp-ts/function';
import { observer } from 'mobx-react';
import React from 'react';
import { useEffect } from 'react';
import { myContainer } from '../../config/inversify.config';
import { TYPES } from '../../typings/types';
import { ErrorSnackbar } from '../Atomics/ErrorSnackbar';
import CamerasList from '../CamerasList/CamerasList';
import ImageInfo from '../ImageInfo/ImageInfo';
import ImageView from '../ImageView/ImageView';
import './Slider.pcss';
import { SliderStore } from './SliderStore';

export interface ISlider {}

export const Slider = observer(() => {
    const sliderStore = myContainer.get<SliderStore>(TYPES.SliderStore);

    useEffect(() => {
        void sliderStore.getCameraList();

        const defaultCameraId = sliderStore.camerasList[0].name;
        if (sliderStore.camerasList.length > 0) {
            void sliderStore.changeCurrentCamera(defaultCameraId);
            void sliderStore.changeCurrentStep(defaultCameraId, getCurrentStep(defaultCameraId));
        }
    }, [])

    const handleCurrentStepChange = (step: number): void => {
        if (sliderStore.camera !== null && step >= 0 && step < sliderStore.camera?.images.length) {
            sliderStore.changeCurrentStep(sliderStore.camera.id, step);
        }
    };

    const getCurrentStep = (cameraId: string): number => {
        const currentStep = sliderStore.stepsStore.getCurrentStep(cameraId);
        return currentStep !== undefined ? currentStep : sliderStore.camera!.images.length - 1;
    };

    const handleCameraChange = async (cameraId: string): Promise<void> => {
        const isCameraExists = sliderStore.camerasList.find((camera) => camera.name == cameraId);
        if (isCameraExists !== undefined) {
            await sliderStore.changeCurrentCamera(cameraId);
            const currentStep = getCurrentStep(cameraId);
            await sliderStore.changeCurrentStep(cameraId, currentStep);
        }
    };


    const keyPressed = (e: KeyboardEvent): void => {
        const data = new Map();

        data.set('ArrowRight', flow(getCurrentStep, increment, handleCurrentStepChange));
        data.set('ArrowLeft', flow(getCurrentStep, decrement, handleCurrentStepChange));
        data.set('ArrowUp', flow(parseInt, decrement, String, handleCameraChange)); // Ужас, надо бы поправить и решить что делать с индексами камер
        data.set('ArrowDown', flow(parseInt, increment, String, handleCameraChange));

        const action = data.get(e.key);
        if (action) {
            action(sliderStore.camera!.id);
        }
    };

    document.addEventListener('keydown', keyPressed, false);
    const { camera } = sliderStore;
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
                        cameras={sliderStore.camerasList}
                        onCameraChange={handleCameraChange}
                    />
                </Grid>
                <Grid item={true}>
                    {!isCameraAvailable && <Alert severity="warning">No camera found</Alert>}
                    {isCameraAvailable && camera && (
                        <ImageView
                            currentStep={getCurrentStep(camera.id)}
                            changeCurrentStep={handleCurrentStepChange}
                            images={camera.images}
                        />
                    )}
                </Grid>
                <Grid item={true}>
                    {camera && isCameraAvailable && sliderStore.imageInfo && (
                        <ImageInfo
                            cameraOnlineDate={new Date(camera.onlineDate)}
                            store={myContainer.get(TYPES.ImageInfoStore)}
                            info={sliderStore.imageInfo}
                        />
                    )}
                </Grid>
                {sliderStore.error && <ErrorSnackbar message={sliderStore.error.message} />}
            </Grid>
        </Card>
    );

 })
