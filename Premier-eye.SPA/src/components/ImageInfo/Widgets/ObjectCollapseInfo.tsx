import { Collapse, List, ListItem } from '@material-ui/core';
import { observer } from 'mobx-react';
import React from 'react';

export interface IObjectCollapseInfo {
    isOpen: boolean;
    scores: number;
}

@observer
export class ObjectCollapseInfo extends React.Component<IObjectCollapseInfo> {
    render() {
        return (
            <Collapse in={this.props.isOpen} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                    <ListItem> Степень уверенности: {(this.props.scores * 100).toFixed(2)}% </ListItem>
                </List>
            </Collapse>
        );
    }
}
