import {API_URL, ApiRoutes} from "../config/apiRoutes";
import {inject, injectable} from "inversify";
import {TYPES} from "../typings/types";
import {Either} from "@sweet-monads/either";
import {IApiInteractionService, IBaseInteractionService} from "./typings/ApiTypes";
import BaseInteractionService from "./BaseInteractionService";
import {AxiosRequestConfig} from "axios";
import {BaseInteractionError} from "./Errors/BaseInteractionError";



@injectable()
class ApiInteractionService  implements IApiInteractionService {
    fetcher: IBaseInteractionService

    constructor(
        @inject(TYPES.BaseInteractionService) baseInteractionService: IBaseInteractionService,
    ) {
        this.fetcher = baseInteractionService
    }

    public async get<T = any>(url: string, data?: any, host: string = API_URL, config?: AxiosRequestConfig): Promise<Either<BaseInteractionError, T>> {
        return this.fetcher.get<T>(url, data, host, config)
    }

    public async post<T = any>(url: string, data?: any, host: string = API_URL, settings?: any, config?: AxiosRequestConfig): Promise<Either<BaseInteractionError, T>> {
        return this.fetcher.post<T>(url, data, host, settings, config)
    }

    public async put<T = any>(url: string, data?: any, host: string = API_URL, settings?: any, config?: AxiosRequestConfig): Promise<Either<BaseInteractionError, T>> {
        return this.fetcher.put<T>(url, data, host, settings, config)
    }

    public async delete<T = any>(url: string, data?: any, host: string = API_URL, config?: AxiosRequestConfig): Promise<Either<BaseInteractionError, T>> {
        return this.fetcher.delete<T>(url, data, host, config)
    }

}

export default ApiInteractionService
