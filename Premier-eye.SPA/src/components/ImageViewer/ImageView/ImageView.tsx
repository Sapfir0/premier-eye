import { observer } from 'mobx-react';
import React from 'react';
import SwipeableViews from 'react-swipeable-views';
import { definitions } from 'typings/Dto';
import { ApiRoutes, API_URL } from '../../../config/apiRoutes';
import './ImageView.pcss';
import { CustomStepper } from './Steppers/CustomStepper';
import { IStepper } from './Steppers/IStepper';

interface IImageView extends IStepper {
    updateStateByInfo: (src: string) => void;
}

@observer
export default class ImageView extends React.Component<IImageView> {
    constructor(props: IImageView) {
        super(props);
    }

    public handleStepChange = (step: number) => {
        this.props.changeCurrentStep(step);
    };

    public render() {
        console.log('reimageView');

        return (
            <div className="imageView">
                <SwipeableViews index={this.props.currentStep} onChangeIndex={this.handleStepChange} enableMouseEvents>
                    {this.props.images.map((image: definitions['Image'], index: number) => (
                        <div key={image.id}>
                            {Math.abs(this.props.currentStep - index) <= 2 ? (
                                <img
                                    className="img"
                                    src={API_URL + ApiRoutes.GALLERY.GET_IMAGE(image.src)}
                                    alt={image.src}
                                />
                            ) : null}
                        </div>
                    ))}
                </SwipeableViews>

                <CustomStepper {...this.props} />
            </div>
        );
    }
}
