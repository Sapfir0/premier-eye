import React from 'react';
import MobileStepper from '@material-ui/core/MobileStepper';
import Button from '@material-ui/core/Button';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import SwipeableViews from 'react-swipeable-views';
import {withStyles} from "@material-ui/core/styles";
import NotFoundImage from "../atoms/NotFoundImage";
import {API_URL, ApiRoutes} from "../../config/apiRoutes";
import {ISliderPublicAction} from "../../typings/IAction";


const styles = {
    imageView: {
        maxWidth: 400,
        flexGrow: 1,
    },
    header: {
        display: 'flex',
        alignItems: 'center',
        height: 50,
    },
    img: {
        height: 255,
        display: 'block',
        maxWidth: 400,
        overflow: 'hidden',
        width: '100%',

        backgroundColor: 'red',
        color: 'white',
    },

}

interface IProps {
    images: Array<string>,
    classes: any,
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
        const {classes} = this.props;

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
                            <img className={classes.img} src={API_URL + ApiRoutes.GALLERY.GET_IMAGE(src)} alt={src}/>
                        ) : null}
                    </div>
                ))}
            </SwipeableViews>
            <MobileStepper
                steps={this.props.images.length}
                position="static"
                variant="progress"
                activeStep={this.props.currentStep}
                nextButton={
                    <Button size="small" onClick={this.handleNext} disabled={this.props.currentStep === this.props.images.length - 1}>
                        Next
                        <KeyboardArrowRight/>
                    </Button>
                }
                backButton={
                    <Button size="small" onClick={this.handleBack} disabled={this.props.currentStep === 0}>
                        <KeyboardArrowLeft/>
                        Back
                    </Button>
                }
            />
            </>
        }

        return (
            <div className={classes.imageView}>
                {slideBlock}
            </div>
        );
    }


}

export default withStyles(styles)(ImageView);
