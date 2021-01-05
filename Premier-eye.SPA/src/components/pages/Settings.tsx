import React from 'react';
import { myContainer } from '../../config/inversify.config';
import { TYPES } from '../../typings/types';
import { SliderStore } from '../ImageViewer/Slider/SliderStore';
import { Settings } from '../Settings/Settings';

export default function SettingsPage() {
    const store = myContainer.get<SliderStore>(TYPES.SliderStore);
    return <Settings sliderStore={store} />;
}
