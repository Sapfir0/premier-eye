
interface ObjectInfo {
    id: number,
    typesOfObject: string,
    scores: number
}

interface IImageInfo {
    numberOfCam: number,
    filename: string,
    fixationDatetime: Date,
    createdAt: Date,
    objects: Array<ObjectInfo>
}


export type { IImageInfo, ObjectInfo}
