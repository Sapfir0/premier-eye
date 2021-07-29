import { Container } from 'inversify';
import 'reflect-metadata';
import { AreaMapStore } from '../components/AreaMap/AreaMapStore';
import { CameraLoggerStore } from '../components/CameraLogger/CameraLoggerStore';
import { ImageInfoStore } from '../components/ImageInfo/ImageInfoStore';
import { SettingsStore } from '../components/Settings/SettingsStore';
import { SliderStore } from '../components/Slider/SliderStore';
import { AreaMapApiInteractionService } from '../services/ApiInteractionService/AreaMapInteractionService';
import CameraApiInteractionService from '../services/ApiInteractionService/CameraApiInteractionService';
import EventApiInteractionService from '../services/ApiInteractionService/EventApiInteractionService';
import GalleryApiInteractionService from '../services/ApiInteractionService/GalleryApiInteractionService';
import { ICameraApiInteractionService, IGalleryApiInteractionService } from '../services/typings/ApiTypes';
import { TYPES } from '../typings/types';

const myContainer = new Container();

myContainer.bind(TYPES.SliderStore).to(SliderStore);
myContainer.bind(TYPES.ImageInfoStore).to(ImageInfoStore);
myContainer.bind(TYPES.SettingsStore).to(SettingsStore);
myContainer.bind(TYPES.AreaMapStore).to(AreaMapStore);
myContainer.bind(TYPES.CameraLoggerStore).to(CameraLoggerStore);

myContainer.bind<IGalleryApiInteractionService>(TYPES.GalleryApiInteractionService).to(GalleryApiInteractionService);
myContainer.bind<ICameraApiInteractionService>(TYPES.CameraApiInteractionService).to(CameraApiInteractionService);
myContainer.bind<EventApiInteractionService>(TYPES.EventApiInteractionService).to(EventApiInteractionService);
myContainer.bind<AreaMapApiInteractionService>(TYPES.AreaMapApiInteractionService).to(AreaMapApiInteractionService);

export { myContainer };
