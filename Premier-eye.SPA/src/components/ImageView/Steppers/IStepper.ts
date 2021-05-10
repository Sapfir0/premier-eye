import { definitions } from '../../../../typings/Dto';

export interface IStepper {
    images: Array<definitions['Image']>;
    currentStep: number;
    changeCurrentStep: (step: number) => void;
}
