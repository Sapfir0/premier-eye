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
import {IUrlService} from "../services/typings/IUrlService";
import UrlService from "../services/UrlService";
import CameraApiInteractionService from "../services/ApiInteractionService/CameraApiInteractionService";
import {SliderStore} from "../components/Slider/SliderStore";

const myContainer = new Container();


myContainer.bind<IApiHelper>(TYPES.ApiHelper).to(ApiHelper)
myContainer.bind<IBaseInteractionService>(TYPES.BaseInteractionService).to(BaseInteractionService)

myContainer.bind<IApiInteractionService>(TYPES.ApiInteractionService).to(ApiInteractionService)

myContainer.bind<IUrlService>(TYPES.UrlService).to(UrlService)

myContainer.bind(TYPES.SliderStore).to(SliderStore)

myContainer.bind<IGalleryApiInteractionService>(TYPES.GalleryApiInteractionService).to(GalleryApiInteractionService)
myContainer.bind<ICameraApiInteractionService>(TYPES.CameraApiInteractionService).to(CameraApiInteractionService)

export { myContainer }