import DirectionsCar from "@material-ui/icons/DirectionsCar";
import PersonIcon from "@material-ui/icons/Person";
import React from "react";

interface ObjectsPictures {
    'icon': JSX.Element,
    'title': string
}

export const detectionsImages: { [objectName: string]: ObjectsPictures } = {
    'car': {'icon': <DirectionsCar/>, 'title': 'Автомобиль'},
    'person': {'icon': <PersonIcon/>, 'title': 'Человек'},
}
