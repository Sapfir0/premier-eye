import DirectionsCar from "@material-ui/icons/DirectionsCar";
import PersonIcon from "@material-ui/icons/Person";
import React from "react";

interface objectsPictures {
    'icon': JSX.Element,
    'title': string
}

const detectionsImages: { [objectName: string]: objectsPictures } = {
    'car': {'icon': <DirectionsCar/>, 'title': 'Автомобиль'},
    'person': {'icon': <PersonIcon/>, 'title': 'Человек'},
}


export {detectionsImages}
