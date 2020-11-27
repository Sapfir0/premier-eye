import { List, ListItem, Collapse } from "@material-ui/core"
import React from "react"
import {observer} from "mobx-react";

export interface IObjectCollapseInfo {
    isOpen: boolean,
    scores: number
}

@observer
export class ObjectCollapseInfo extends React.Component<IObjectCollapseInfo>{
   render() {
       return <Collapse
           in={this.props.isOpen}
           timeout="auto"
           unmountOnExit
       >
           <List component="div" disablePadding>
               <ListItem> Степень уверенности: {this.props.scores * 100}% </ListItem>
           </List>
       </Collapse>
   }
}