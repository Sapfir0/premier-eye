import { io } from 'socket.io-client';
import { API_URL } from '../config/apiRoutes';

export const socket = io(API_URL);


