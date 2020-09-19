export const API_URL = process.env.API_URL || "http://localhost:8050"


const GALLERY_HIGH_LEVEL_DOMAIN = "/gallery"


const GALLERY = {
    GET_INFO_IMAGE: (imageName: string) => `${GALLERY_HIGH_LEVEL_DOMAIN}/${imageName}/info`,
    GET_IMAGES_FROM_CAMERA: (cameraId: number) => `${GALLERY_HIGH_LEVEL_DOMAIN}/camera/${cameraId}`,
    GET_IMAGE: (imageName: string) => `${GALLERY_HIGH_LEVEL_DOMAIN}/${imageName}`,
    GET_ALL_IMAGES: `${GALLERY_HIGH_LEVEL_DOMAIN}/gallery`,
    GET_CAMERA_INFO: (cameraId: number) => `${GALLERY_HIGH_LEVEL_DOMAIN}/camera/${cameraId}`
}


export const ApiRoutes = { GALLERY } as const


