// get elements
const loginForm = document.querySelector('.login');
const loginSubmitButton = loginForm.querySelector('.login__submit');
const loginUserNameInput = loginForm.querySelector('input[type="text"]');
const loginPasswordInput = loginForm.querySelector('input[type="password"]');

// add event listener to login submit button
loginSubmitButton.addEventListener('click', (e) => {
  e.preventDefault(); // prevent form from submitting

  const userName = loginUserNameInput.value;
  const password = loginPasswordInput.value;

  // send login request to server
  console.log("handling the request")
  fetch('/auth/login', {
    
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: userName,
      password: password
    })
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Invalid username or password');
    }
  })
  .then(data => {
    // store token in local storage
    localStorage.setItem('token', data.token);
    // redirect to home page or any other page
    window.location.href = '/model/text';
  })
  .catch(error => {
    console.log(error);
    // display error message to user
    alert(error.message);
  });
});
