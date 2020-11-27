import { List, ListItem, Collapse } from "@material-ui/core"
import React from "react"


export const ObjectCollapseInfo = (isOpen: boolean, scores: number) => (
    <Collapse
        in={isOpen}
        timeout="auto"
        unmountOnExit
    >
        <List component="div" disablePadding>
            <ListItem> Степень уверенности: {scores * 100}% </ListItem>
        </List>
    </Collapse>
)