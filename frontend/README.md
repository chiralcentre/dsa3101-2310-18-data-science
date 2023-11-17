# Frontend

This directory contains the frontend codebase for DataGuru Project. This README serves as a guide to setting up and running the frontend application.

## Introduction

Welcome to the frontend folder of DataGuru. This directory holds the code responsible for the user interface and presentation layer of our application.

## Folder Structure

The frontend directory structure is as follows: 

```
frontend/
├── public/
│   ├── img/
│   ├── index.html
│   ├── logo192.png
│   ├── manifest.json
│   └── robots.txt
├── src/
│   └── components/
│       ├── App.js
│       ├── index.css
│       └── index.js
├── .gitignore
├── README.md
├── package-lock.json
├── package.json
```
- `public`  store static assets that don’t go through the build process 
- `src` contains JavaScript (.js) and CSS (.css) files which will be processed by the
web pack
- `App.js` contains the main logic for routing in the application
- `index.css` stylesheet file that contains global styles for the React
application, providing consistent styling across different components and
pages
- `package.json` contains metadata about project details and dependencies for
defining project settings and specifying required packages

To set up the frontend locally, follow these steps:

1. Clone the repository.
2. Navigate to the frontend directory.
3. Run `npm install` to install the necessary dependencies.
4. Run `npm run start` to start the development for the web app application.

Up to this step, you will be able to see the web app running at http://localhost:3000/. However, this web application will not be integrated with the backend API. To see the integrated version, follow the additional steps below: 
1. Navigate to the backend directory.
2. Run `flask --app launch --debug run`.
3. Refresh your React application. 

Now, you will be able to see the fully integrated version of the web app. 

