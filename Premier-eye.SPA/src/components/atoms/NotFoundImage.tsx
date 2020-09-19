import React from "react";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    error: {

    },
    img: {

    }

}));

export default function NotFoundImage() {
    const classes = useStyles();

    return(<div className={classes.img}>
        К сожалению, изображения с этой камеры не найдена
    </div>)

}
