export const API_URL = process.env.API_URL || 'http://localhost:8050';

const GALLERY_HIGH_LEVEL_DOMAIN = '/gallery';
const GALLERY = {
    GET_IMAGE: (imageName: string) => `${GALLERY_HIGH_LEVEL_DOMAIN}/image/${imageName}`,
    GET_ALL_IMAGES: `${GALLERY_HIGH_LEVEL_DOMAIN}/images`,
};

const IMAGE_INFO_HIGH_LEVEL_DOMAIN = '/imageInfo';
const IMAGE_INFO = {
    GET_INFO_IMAGE: (imageName: string) => `${IMAGE_INFO_HIGH_LEVEL_DOMAIN}/${imageName}/info`,
    GET_IMAGE_INFO_BY_INDEX: `${IMAGE_INFO_HIGH_LEVEL_DOMAIN}/info`,
};

const MATH_HIGH_LEVEL_DOMAIN = '/math';
const MATH = {
    GET_IMAGE_BETWEEEN_DATES_FROM_CAMERA: (cameraId: number) => `${MATH_HIGH_LEVEL_DOMAIN}/cameraDelta${cameraId}`,
    GET_OBJECTS_FROM_RECTANGLE_ON_IMAGE: (src: string) => `${MATH_HIGH_LEVEL_DOMAIN}/${src}/objects`,
    GET_OBJECTS_FROM_RECTANGLE_ON_IMAGE_VISUALIZE: (src: string) => `${MATH_HIGH_LEVEL_DOMAIN}/${src}/objectsVisualize`,
};

const CAMERA_HIGH_LEVEL_DOMAIN = '/camera';
const CAMERA = {
    GET_ALL_IMAGES_FROM_CAMERA: (cameraId: string) => `${CAMERA_HIGH_LEVEL_DOMAIN}/${cameraId}`,
    GET_CAMERAS_LIST: `${CAMERA_HIGH_LEVEL_DOMAIN}/list`,
    CAMERA: `${CAMERA_HIGH_LEVEL_DOMAIN}/`,
};

export const ApiRoutes = { GALLERY, CAMERA, IMAGE_INFO, MATH } as const;
