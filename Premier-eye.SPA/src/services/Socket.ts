import { injectable } from 'inversify';
import { io, Socket } from 'socket.io-client';
import { API_URL } from '../config/apiRoutes';

@injectable()
export class ImageUpdateWS {
    private _socket: Socket;

    constructor() {
        this._socket = io(API_URL);
    }

    public createChannel = (): void => {
        this._socket.on('connect', () => {
            console.log(this._socket, this._socket.connected);
        });

        this._socket.onAny((...args) => {
            console.log(args);
        });
        this._socket.on('imageUpdated', (...args) => {
            console.log(args);
        });
    };
}
