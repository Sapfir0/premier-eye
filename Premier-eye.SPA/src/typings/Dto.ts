/**
 * This file was auto-generated by swagger-to-ts.
 * Do not make direct changes to the file.
 */

export interface definitions {
  ImageList: { items: string[] };
  CameraImageList: { items: string[] };
  ImageInfo: {
    numberOfCam: number;
    filename: string;
    fixationDatetime: string;
    createdAt: string;
    objects: definitions["ObjectInfo"][];
  };
  ObjectInfo: { id: number; type: string; scores: number };
}
