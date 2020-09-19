
export const GET_IMAGES_FROM_CAMERA = "GET_IMAGES_FROM_CAMERA" as const
export const SET_IMAGES_FROM_CAMERA = "SET_IMAGES_FROM_CAMERA" as const

export const CHANGE_CURRENT_STEP = "CHANGE_CURRENT_STEP" as const
export const CHANGE_CURRENT_CAMERA = "CHANGE_CURRENT_CAMERA" as const


export const GET_INFO_IMAGE = "GET_INFO_IMAGE" as const
export const SET_INFO_IMAGE = "SET_INFO_IMAGE" as const

export const SET_SLIDER_ERROR = "SET_SLIDER_ERROR" as const
export const UNSET_SLIDER_ERROR = "UNSET_SLIDER_ERROR" as const

const sliderActions = {
    GET_IMAGES_FROM_CAMERA, SET_IMAGES_FROM_CAMERA,
    GET_INFO_IMAGE, SET_INFO_IMAGE, CHANGE_CURRENT_STEP,
    SET_SLIDER_ERROR, UNSET_SLIDER_ERROR,
    CHANGE_CURRENT_CAMERA,
} as const

export type SLIDER_ACTIONS = typeof sliderActions[keyof typeof sliderActions]
