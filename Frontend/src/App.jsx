import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Projects from './pages/projcts'
import CreateProject from './pages/create_projects'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { purple } from '@mui/material/colors'
import Layout from './components/Layout'


const theme = createTheme({
  palette: {
    primary: {
      main: '#fefefe'
    },
    secondary: {
      main: '#9500ae'
    }
  },
  typography: {
    fontFamily: 'Quicksand',
    fontWeightLight: 400,
    fontWeightRegular: 500,
    fontWeightMedium: 600,
    fontWeightBold: 700,
  },
  MuiAppBar:{
    colorPrimary: "red",
  }
})

function App() {
  return (
    <ThemeProvider theme={theme}>
    <Router>
      <Layout>
        <Switch>
          <Route path="/create">
            <CreateProject />
          </Route>
        </Switch>
      </Layout>
      </Router>
  </ThemeProvider>
  );
}

export default App;
