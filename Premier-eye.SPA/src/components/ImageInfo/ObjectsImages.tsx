
import React from "react";
import {Icon} from "semantic-ui-react";

interface objectsPictures {
    'icon': JSX.Element,
    'title': string
}

const detectionsImages: { [objectName: string]: objectsPictures } = {
    'car': {'icon': <Icon name="car"/>, 'title': 'Автомобиль'},
    'person': {'icon': <Icon name="users"/>, 'title': 'Человек'},
}


export {detectionsImages}
