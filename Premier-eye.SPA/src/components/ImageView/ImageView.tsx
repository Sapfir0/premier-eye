import React from 'react';
import SwipeableViews from 'react-swipeable-views';
import NotFoundImage from "../atoms/NotFoundImage";
import {API_URL, ApiRoutes} from "../../config/apiRoutes";
import {ISliderPublicAction} from "../../typings/IAction";
import {Button, Icon} from "semantic-ui-react";



interface IProps {
    images: Array<string>,
    updateStateByInfo: (src: string) => void
    changeCurrentStep: (step: number) => void
    currentStep: number
}



class ImageView extends React.Component<IProps> {
    constructor(props: IProps) {
        super(props);
    }

    handleNext = () => { // для кнопок
        this.props.changeCurrentStep(this.props.currentStep+1)
    };

    handleBack = () => { // для кнопок
        this.props.changeCurrentStep(this.props.currentStep-1)
    };

    handleStepChange = (step: number) => {
        this.props.changeCurrentStep(step)
    };

    render() {
        // const {classes} = this.props;

        let slideBlock;
        if(this.props.images.hasOwnProperty("error")) {
            slideBlock = <NotFoundImage />
        }
        else {
            slideBlock = <> <SwipeableViews
                index={this.props.currentStep}
                onChangeIndex={this.handleStepChange}
                enableMouseEvents
            >
                {this.props.images.map((src: string, index: number) => (
                    <div key={src}>
                        {Math.abs(this.props.currentStep - index) <= 2 ? (
                            <img  src={API_URL + ApiRoutes.GALLERY.GET_IMAGE(src)} alt={src}/>
                        ) : null}
                    </div>
                ))}
            </SwipeableViews>
            {/*<MobileStepper*/}
            {/*    steps={this.props.images.length}*/}
            {/*    position="static"*/}
            {/*    variant="progress"*/}
            {/*    activeStep={this.props.currentStep}*/}
            {/*    nextButton={*/}
            {/*        <Button size="small" onClick={this.handleNext} disabled={this.props.currentStep === this.props.images.length - 1}>*/}
            {/*            Next*/}
            {/*            <Icon name="arrow right" />*/}
            {/*        </Button>*/}
            {/*    }*/}
            {/*    backButton={*/}
            {/*        <Button size="small" onClick={this.handleBack} disabled={this.props.currentStep === 0}>*/}
            {/*            <Icon name="arrow left" />*/}
            {/*            Back*/}
            {/*        </Button>*/}
            {/*    }*/}
            {/*/>*/}
            </>
        }

        return (
            <div>
                {slideBlock}
            </div>
        );
    }


}

export default ImageView
