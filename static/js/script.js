// Form Validation for Sign-Up and Login Pages
function validateSignUpForm() {
  // Get form elements
  const firstName = document.getElementById('firstName');
  const lastName = document.getElementById('lastName');
  const age = document.getElementById('age');
  const username = document.getElementById('username');
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirmPassword');

  // Basic validation checks (add more as needed)
  if (firstName.value.trim() === '') {
    alert('Please enter your first name.');
    firstName.focus();
    return false;
  }

  if (lastName.value.trim() === '') {
    alert('Please enter your last name.');
    lastName.focus();
    return false;
  }

  if (age.value.trim() === '' || isNaN(age.value) || age.value < 0) {
    alert('Please enter a valid age.');
    age.focus();
    return false;
  }

  if (username.value.trim() === '') {
    alert('Please enter a username.');
    username.focus();
    return false;
  }

  if (password.value.trim() === '') {
    alert('Please enter a password.');
    password.focus();
    return false;
  }

  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match.');
    confirmPassword.focus();
    return false;
  }

  // If all validations pass, return true to submit the form
  return true;
}

function validateLoginForm() {
  // Get form elements
  const username = document.getElementById('username');
  const password = document.getElementById('password');

  // Basic validation checks
  if (username.value.trim() === '') {
    alert('Please enter your username.');
    username.focus();
    return false;
  }

  if (password.value.trim() === '') {
    alert('Please enter your password.');
    password.focus();
    return false;
  }

  // If all validations pass, return true to submit the form
  return true;
}

// Dynamic Content Updates

// Course Detail Page: Expand/Collapse Modules
function toggleModule(moduleId) {
  const moduleContent = document.getElementById(moduleId);
  if (moduleContent.style.display === 'none') {
    moduleContent.style.display = 'block';
  } else {
    moduleContent.style.display = 'none';
  }
}

// Enrolled Course Page: Update Current Lesson (Example - needs more context)
function updateCurrentLesson(lessonId) {
  // In a real application, you would likely fetch lesson content
  // and update the main content area dynamically.
  console.log('Current Lesson ID:', lessonId);
  // Example update:
  const lessonTitle = document.getElementById('lessonTitle');
  if (lessonTitle) {
    lessonTitle.textContent = `Lesson ${lessonId}`;
  }

  // Highlight the current lesson in the sidebar (requires sidebar structure)
  const sidebarLinks = document.querySelectorAll('.sidebar a'); // Adjust selector as needed
  sidebarLinks.forEach(link => {
      link.classList.remove('active'); // Remove active class from all links
      if (link.dataset.lessonId == lessonId) {
          link.classList.add('active'); // Add active class to the current lesson
      }
  });
}

// Smooth Navigation (example - can be improved with a library)
function smoothScroll(targetId) {
  const targetElement = document.getElementById(targetId);
  if (targetElement) {
    targetElement.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }
}

// Event Listeners (examples - adapt to your HTML structure)

// Sign-Up Form
const signUpForm = document.getElementById('signUpForm');
if (signUpForm) {
  signUpForm.addEventListener('submit', function(event) {
    if (!validateSignUpForm()) {
      event.preventDefault(); // Prevent form submission if validation fails
    }
  });
}

// Login Form
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', function(event) {
    if (!validateLoginForm()) {
      event.preventDefault(); // Prevent form submission if validation fails
    }
  });
}


// Course Detail Page: Example listener for module toggles
const moduleButtons = document.querySelectorAll('.module-toggle'); // Adjust selector as needed
moduleButtons.forEach(button => {
  button.addEventListener('click', function() {
    const moduleId = this.dataset.moduleId;  // Assuming a data-module-id attribute
    toggleModule(moduleId);
  });
});


// Enrolled Course Page: Example listener for sidebar links
const sidebarLinks = document.querySelectorAll('.sidebar a');  // Adjust selector as needed
sidebarLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        const lessonId = this.dataset.lessonId;  // Assuming a data-lesson-id attribute
        updateCurrentLesson(lessonId);
        // Optionally, update the URL to reflect the current lesson
        // window.history.pushState({}, '', `enrolled_course.html?lesson=${lessonId}`);
    });
});


// You'll need to add more listeners and adapt these examples to
// match the specific elements and IDs in your HTML.