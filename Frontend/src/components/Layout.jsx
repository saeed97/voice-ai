import React from 'react'
import { Avatar, Drawer, Grid, Typography} from '@mui/material'
import { makeStyles } from "@mui/styles"
import { useHistory, useLocation } from 'react-router-dom'
import AppBar from "@mui/material/AppBar";
import Toolbar from '@mui/material/Toolbar'
import IconButton from "@mui/material/IconButton";
import MenuIcon from '@mui/icons-material/Menu';
import Box from "@mui/material/Box";
import Menu from "./menu"
import "./Layout.css"

const drawerWidth = 240

const useStyles = makeStyles((theme) => {
  return {
    toolbar: theme.mixins.toolbar,
    page: {
      background: '#f9f9f9',
      width: '100%',
      padding: theme.spacing(3)
    },
    root: {
      display: 'flex'
    },
    drawer1: {
      width: drawerWidth,
      display: { xs: "block", sm: "none" },
      "& .MuiDrawer-paper": {
      boxSizing: "border-box",
      }
    },
    drawer2: {
      width: drawerWidth,
      display: { xs: "none", sm: "block" },
      "& .MuiDrawer-paper": {
      boxSizing: "border-box",
      }
    },
    appBar: {
      width: { sm: `calc(100% - ${drawerWidth}px)` },
      ml: { sm: `${drawerWidth}px` }
    },
    drawerPaper:{
      width: drawerWidth,
    },
    title: {
      padding: theme.spacing(2)
    },

  }
})

export default function Layout({ children }) {
  const classes = useStyles()
  
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <div className={classes.root}>
      {/* app bar */}
      <Box sx={{ display: "flex" }}>
        {/* <CssBaseline /> */}
        <AppBar
          position="fixed"
          sx={{
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            ml: { sm: `${drawerWidth}px` },
          }}
        >
          <Toolbar>
            <Grid 
              container
              justifyContent="center"
              spacing={2}
              padding="2"
            >
              <Grid item flexGrow="1">
                <IconButton
                  color="inherit"
                  aria-label="open drawer"
                  edge="start"
                  onClick={handleDrawerToggle}
                  sx={{ mr: 2, display: { sm: "none" } }}
                >
                  <MenuIcon color="primary"/>
                </IconButton>
              </Grid>
              <Grid item justifyContent="flex-end" >
                <Avatar className={classes.avatar} src="/mario-av.png" />
              </Grid>
            </Grid>
          </Toolbar>
        </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true // Better open performance on mobile.
          }}
          sx={{
            display: { xs: "block", sm: "none" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth
            }
          }}
        >
          <Menu handleDrawerToggle={handleDrawerToggle}/>
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: "none", sm: "block" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth
            }
          }}
          open
        >
          <Menu  handleDrawerToggle={handleDrawerToggle}/>
        </Drawer>
      </Box>
    </Box>
      {/* main content */}
      <div className={classes.page}>
        <div className={classes.toolbar}></div>
        { children }
      </div>
    </div>
  )
}
