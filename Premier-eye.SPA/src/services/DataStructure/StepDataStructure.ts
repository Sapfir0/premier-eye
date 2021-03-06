type CameraId = string;
type CurrentStep = number;

export default class StepDataStructure {
    steps: Map<CameraId, CurrentStep>;
    constructor(camerasCount?: number) {
        this.steps = new Map<CameraId, CurrentStep>();

        if (camerasCount !== undefined) {
            for (let i = 0; i < camerasCount; i++) {
                this.steps.set(i.toString(), 0);
            }
        }
    }

    public getCurrentStep = (cameraId: CameraId) => {
        const step = this.steps.get(cameraId);
        return step === undefined ? 0 : step;
    };

    public changeStepOnCurrentCamera = (cameraId: CameraId, currentStep: CurrentStep) => {
        this.steps.set(cameraId, currentStep);
        return new Map(this.steps);
    };
}
