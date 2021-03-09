/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface definitions {
  ImageList: { items: definitions["Image"][] };
  Image: { id: string; src: string };
  CameraDto: { name: string };
  Camera: {
    id: string;
    name?: string;
    onlineDate: string;
    images: definitions["Image"][];
  };
  CameraList: { items: definitions["Camera"][] };
  ImageInfo: {
    numberOfCam: number;
    filename: string;
    fixationDatetime: string;
    createdAt: string;
    objects: definitions["ObjectInfo"][];
  };
  ObjectInfo: {
    id: string;
    type: string;
    scores: number;
    coordinates: string[];
  };
  DTOLog: { title: string; timestamp: string; cameraId?: number };
  DTOLogs: { titles: string[]; timestamp: string; cameraId: number };
}
