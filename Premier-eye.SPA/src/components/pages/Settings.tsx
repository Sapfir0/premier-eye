import React from 'react';
import { myContainer } from '../../config/inversify.config';
import { TYPES } from '../../typings/types';
import { Settings } from '../Settings/Settings';
import { SettingsStore } from '../Settings/SettingsStore';

export default function SettingsPage() {
    const store = myContainer.get<SettingsStore>(TYPES.SettingsStore);
    return <Settings sliderStore={store} />;
}
