import { List, ListItem, ListItemIcon, ListItemText, Typography } from "@mui/material";
import { AddCircleOutlineOutlined, SubjectOutlined } from '@mui/icons-material'
import { useHistory, useLocation } from 'react-router-dom'
import { makeStyles } from "@mui/styles"
import React from "react";

const useStyle = makeStyles({
  active: {
    backgroundColor: "gray"
  }

})

function Menu(props) {
  const history = useHistory()
  const classes = useStyle()
  const location = useLocation()


  const menuItems = [
      { 
        text: 'Projects', 
        icon: <SubjectOutlined color="secondary" />, 
        path: '/' 
      },
      { 
        text: 'Create Project', 
        icon: <SubjectOutlined color="secondary" />, 
        path: '/create' 
      },
    ];

  const handleClick = (path) => {
    console.log(typeof props.handleDrawerToggle);
    props.handleDrawerToggle()
    history.push(path)
  }

  return ( 
    <div>
      <Typography
          variant="h6"
          noWrap
          align="center" // change to align for centering
          ml="2"
          className="title"
        >
          Voice Generator
        </Typography>
      <List>
        {menuItems.map((item)=>(
          <ListItem
          button
          key={item.text}
          onClick={()=> handleClick(item.path)}
          className={location.pathname==item.path ? null : classes.active}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
    
      </List>
    </div>

    );
}

export default Menu;