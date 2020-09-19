
type CameraId = number
type CurrentStep = number

export default class StepDataStructure {
    steps: Map<CameraId, CurrentStep>
    constructor() {
        this.steps = new Map<CameraId, CurrentStep>()
    }


    getCurrentStep = (cameraId: CameraId) => {
        return this.steps.get(cameraId)
    }

    changeStepOnCurrentCamera = (cameraId: CameraId, currentStep: CurrentStep) => {
        this.steps.set(cameraId, currentStep)
        return new Map(this.steps)
    }

}