import { Container } from 'inversify';
import 'reflect-metadata';
import { AreaMapStore } from '../components/AreaMap/AreaMapStore';
import { ImageInfoStore } from '../components/ImageInfo/ImageInfoStore';
import { SliderStore } from '../components/ImageViewer/Slider/SliderStore';
import ApiHelper from '../services/ApiHelper';
import ApiInteractionService from '../services/ApiInteractionService';
import CameraApiInteractionService from '../services/ApiInteractionService/CameraApiInteractionService';
import GalleryApiInteractionService from '../services/ApiInteractionService/GalleryApiInteractionService';
import BaseInteractionService from '../services/BaseInteractionService';
import {
    IApiHelper,
    IApiInteractionService,
    IBaseInteractionService,
    ICameraApiInteractionService,
    IGalleryApiInteractionService,
} from '../services/typings/ApiTypes';
import { TYPES } from '../typings/types';
import { SettingsStore } from '../components/Settings/SettingsStore';
import { CameraLoggerStore } from '../components/CameraLogger/CameraLoggerStore';
import EventApiInteractionService from '../services/ApiInteractionService/EventApiInteractionService';

const myContainer = new Container();

myContainer.bind<IApiHelper>(TYPES.ApiHelper).to(ApiHelper);
myContainer.bind<IBaseInteractionService>(TYPES.BaseInteractionService).to(BaseInteractionService);

myContainer.bind<IApiInteractionService>(TYPES.ApiInteractionService).to(ApiInteractionService);

myContainer.bind(TYPES.SliderStore).to(SliderStore);
myContainer.bind(TYPES.ImageInfoStore).to(ImageInfoStore);
myContainer.bind(TYPES.SettingsStore).to(SettingsStore);
myContainer.bind(TYPES.AreaMapStore).to(AreaMapStore);
myContainer.bind(TYPES.CameraLoggerStore).to(CameraLoggerStore);

myContainer.bind<IGalleryApiInteractionService>(TYPES.GalleryApiInteractionService).to(GalleryApiInteractionService);
myContainer.bind<ICameraApiInteractionService>(TYPES.CameraApiInteractionService).to(CameraApiInteractionService);
myContainer.bind<EventApiInteractionService>(TYPES.EventApiInteractionService).to(EventApiInteractionService);

export { myContainer };
