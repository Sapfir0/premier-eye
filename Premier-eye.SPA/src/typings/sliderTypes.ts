export type ObjectsColorsWithType<T extends symbol | string> = {
    [P in T]: string;
};

export type ObjectTypes = 'car' | 'person';

export type ObjectColors = ObjectsColorsWithType<ObjectTypes>;
