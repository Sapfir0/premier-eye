import { AxiosResponse } from 'axios';
import { Either, left, right } from 'fp-ts/Either';
import { injectable } from 'inversify';
import { NetworkError } from './Errors/NetworkError';
import { IApiHelper } from './typings/ApiTypes';

@injectable()
class ApiHelper implements IApiHelper {
    public request = async <T>(promise: Promise<AxiosResponse<T>>): Promise<Either<NetworkError, any>> => {
        // на самом деле, это должна быть генераторная функци но мне лень ее биндить ручками
        try {
            const data = await promise;
            return right<NetworkError, AxiosResponse<T>>(data);
        } catch (e) {
            const error = { ...e };
            console.warn(error);
            return left<NetworkError, AxiosResponse<T>>(new NetworkError(error.response?.data.error ?? 'Null error'));
        }
    };
}

export default ApiHelper;
