import React from "react";
import {Icon, Popup} from "semantic-ui-react";


export default function TitledWarning(props: { text: string; }) {
    const longText = props.text;
    return (<Popup title={longText} aria-label="add">
        <Icon name="warning sign" color="orange" />
    </Popup>)
}
