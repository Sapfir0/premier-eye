import StepDataStructure from '../services/DataStructure/StepDataStructure';
import { IdPayload } from './common';
import { definitions } from './Dto';

export type ImagesUrlPayload = {
    imagesUrl: string[];
};

export type ChangeStepPayload = {
    cameraId: number;
    currentStep: number;
};

export type ImagesInfoPayload = {
    imageInfo: definitions['ImageInfo'];
};

export type SrcPayload = {
    src: string;
};

export type SliderBasePayload = ImagesInfoPayload & ImagesUrlPayload & SrcPayload & ChangeStepPayload & IdPayload;

export type ISliderStore = {
    imageInfo: definitions['ImageInfo'] | null;
    imagesList: Array<string>;
    currentCameraId: number;
    stepsStore: StepDataStructure;
    stepMap: Map<number, number>;
};
