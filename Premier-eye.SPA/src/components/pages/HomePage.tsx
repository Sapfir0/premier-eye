import React from 'react';
import { myContainer } from '../../config/inversify.config';
import { TYPES } from '../../typings/types';
import Slider from '../ImageViewer/Slider/Slider';

export default function HomePage() {
    return (
        <>
            <Slider store={myContainer.get(TYPES.SliderStore)} />
        </>
    );
}
