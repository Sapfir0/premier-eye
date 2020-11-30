import React from 'react';
import NotFoundImage from "../Atomics/NotFoundImage";
import "./ImageView.pcss"
import {ISliderBlock, SlideBlock} from "./SliderBlock"


interface IImageView extends ISliderBlock {
    updateStateByInfo: (src: string) => void
}

export default class ImageView extends React.Component<IImageView> {
    constructor(props: IImageView) {
        super(props);
    }

    public handleStepChange = (step: number) => {
        this.props.changeCurrentStep(step)
    };

    public render() {
        let slideBlock;
        if (this.props.images.hasOwnProperty("error")) {
            slideBlock = <NotFoundImage />
        }
        else {
            slideBlock = <SlideBlock {...this.props} />
        }

        return (
            <div className="imageView">
                {slideBlock}
            </div>
        );
    }
}
