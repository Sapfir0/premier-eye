import {AxiosError, AxiosResponse} from "axios";
import {injectable} from "inversify";
import ClientRoutes from "../config/clientRoutes";
import {Either, left, right} from "@sweet-monads/either";
import {IApiHelper} from "./typings/ApiTypes";
import {NetworkError} from "./Errors/NetworkError";


@injectable()
class ApiHelper implements IApiHelper {

    public request = async <T>(promise: Promise<AxiosResponse<T>>): Promise<Either<NetworkError, any>> => { // на самом деле, это должна быть генераторная функци но мне лень ее биндить ручками
        try {
            const data = await promise
            return right<NetworkError, AxiosResponse<T>>(data)
        }
        catch (e) {
            const error = {...e}
            console.warn(error)
            return left<NetworkError, AxiosResponse<T>>(new NetworkError(error.response?.data ?? "Null error"))
        }
    }
}

export default ApiHelper

