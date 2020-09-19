import {ClientRouteType} from "../../config/clientRoutes";

export class BaseInteractionError extends Error {
    message: string

    constructor(message: string) {
        super();
        this.name = "BaseInteractionError"
        this.message = message


    }}
