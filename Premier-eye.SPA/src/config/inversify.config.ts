import "reflect-metadata";
import ApiHelper from "../services/ApiHelper";
import {TYPES} from "../typings/types";
import {
    IApiHelper,
    IApiInteractionService,
    IBaseInteractionService, ICameraApiInteractionService,
    IGalleryApiInteractionService
} from "../services/typings/ApiTypes";
import {Container} from "inversify";
import BaseInteractionService from "../services/BaseInteractionService";
import ApiInteractionService from "../services/ApiInteractionService";
import GalleryApiInteractionService from "../services/ApiInteractionService/GalleryApiInteractionService";
import CameraApiInteractionService from "../services/ApiInteractionService/CameraApiInteractionService";
import {SliderStore} from "../components/ImageViewer/Slider/SliderStore";
import { ImageInfoStore } from "../components/ImageInfo/ImageInfoStore";
import { AreaMapStore } from "../components/AreaMap/AreaMapStore";

const myContainer = new Container();


myContainer.bind<IApiHelper>(TYPES.ApiHelper).to(ApiHelper)
myContainer.bind<IBaseInteractionService>(TYPES.BaseInteractionService).to(BaseInteractionService)

myContainer.bind<IApiInteractionService>(TYPES.ApiInteractionService).to(ApiInteractionService)

myContainer.bind(TYPES.SliderStore).to(SliderStore)
myContainer.bind(TYPES.ImageInfoStore).to(ImageInfoStore)

myContainer.bind<IGalleryApiInteractionService>(TYPES.GalleryApiInteractionService).to(GalleryApiInteractionService)
myContainer.bind<ICameraApiInteractionService>(TYPES.CameraApiInteractionService).to(CameraApiInteractionService)

myContainer.bind(TYPES.AreaMapStore).to(AreaMapStore)

export { myContainer }