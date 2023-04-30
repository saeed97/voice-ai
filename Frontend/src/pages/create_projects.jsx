import { Box, Button, FormControl, FormControlLabel, FormGroup, FormLabel, Radio, RadioGroup, TextField, Typography } from '@mui/material'
import { Container } from '@mui/system'
import React, { useState } from 'react'
import { KeyboardArrowRightRounded} from '@mui/icons-material';
import { useHistory } from 'react-router-dom'
import { makeStyles } from "@mui/styles"
import "./pages.css"

const useStyles = makeStyles({

})

export default function CreateProject() {
//   const classes = useStyles()
  const history = useHistory()
  const [title, setTitle] = useState('')
  const [details, setDetails] = useState('')
  const [titleError, setTitleError] = useState(false)
  const [detailsError, setDetailsError] = useState(false)
  const [category, setCategory] = useState('money')

  const handleSubmit = (e) => {
    e.preventDefault()
    setTitleError(false)
    setDetailsError(false)

    if (title == '') {
      setTitleError(true)
    }
    if (details == '') {
      setDetailsError(true)
    }
    if (title && details) {
      fetch('http://localhost:8000/notes', {
        method: 'POST',
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({ title, details, category })
      }).then(() => history.push('/'))
    } 
  }

  return (
    <Container size="sm" style={{flexDirection: "columns"}}>
      <Typography
        variant="h6" 
        color="textSecondary"
        component="h2"
        gutterBottom
      >
        Create a New Voice Project
      </Typography>
      
      <form noValidate autoComplete="off" onSubmit={handleSubmit}>
        <TextField slotProps={{ field: { className: 'field' } }}
          onChange={(e) => setTitle(e.target.value)}
          label="Note Title" 
          variant="outlined" 
          color="secondary" 
          fullWidth
          required
          error={titleError}
        />
        <TextField slotProps={{ field: { className: 'field' } }}
          style={{marginTop: "20px", marginBottom: "20px"}}
          onChange={(e) => setDetails(e.target.value)}
          label="Details"
          variant="outlined"
          color="secondary"
          multiline
          rows={4}
          fullWidth
          required
          error={detailsError}
        />

        {/* <Radio value="hello" />
        <Radio value="goodbye" /> */}

        <FormControl slotProps={{ field: { className: 'field' } }} style={{display: 'block'}}>
          <FormLabel>Note Category</FormLabel>
          <RadioGroup value={category} onChange={(e) => setCategory(e.target.value)}>
            <FormControlLabel value="money" control={<Radio color="secondary"/>} label="Money" />
            <FormControlLabel value="todos" control={<Radio color="secondary"/>} label="Todos" /> 
            <FormControlLabel value="reminders" control={<Radio color="secondary"/>} label="Reminders" />
            <FormControlLabel value="work" control={<Radio color="secondary"/>} label="Work" />
          </RadioGroup>
        </FormControl>

        <Box display='flex' justifyContent='center'>
          <Button
            type="submit" 
            color="secondary" 
            variant="contained"
            className="button"
            endIcon={<KeyboardArrowRightRounded />}>
            Submit
          </Button>
        </Box>
      </form>

      
    </Container>
  )
}
