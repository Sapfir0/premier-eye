import {ClientRouteType} from "../../config/clientRoutes";

export class NetworkError extends Error {
    message: string

    constructor(message: string) {
        super();
        this.name = "NetworkError"
        this.message = message ?? "Undefined Error with request"

    }
}
