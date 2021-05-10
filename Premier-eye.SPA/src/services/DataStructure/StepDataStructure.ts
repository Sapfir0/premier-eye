import { Map } from 'immutable';

type CameraId = string;
type CurrentStep = number;

export default class StepDataStructure {
    steps: Map<CameraId, CurrentStep>;
    constructor(camerasCount?: number) {
        this.steps = Map<CameraId, CurrentStep>();

        if (camerasCount !== undefined) {
            for (let i = 0; i < camerasCount; i++) {
                this.steps.set(i.toString(), 0);
            }
        }
    }

    public getCurrentStep = (cameraId: CameraId) => {
        return this.steps.get(cameraId);
    };

    public changeStepOnCurrentCamera = (cameraId: CameraId, currentStep: CurrentStep) => {
        this.steps = this.steps.set(cameraId, currentStep);
        return this.steps;
    };
}
