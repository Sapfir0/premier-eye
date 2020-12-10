import React from "react";
import {AreaMap} from "../AreaMap/AreaMap";
import {myContainer} from "../../config/inversify.config";
import {TYPES} from "../../typings/types";


export default function AreaMapPage() {
    return (
        <>
            <AreaMap areaStore={myContainer.get(TYPES.AreaMapStore)}/>
        </>

    )
}



