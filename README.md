# Course Creation API

A Flask-based REST API for managing courses in an educational institution.

## Features

- Create new courses (Admin only)
- Retrieve all courses
- Get course by code
- Delete courses

## API Endpoints

### Create Course
- **POST** `/courses/create`
- **Body**: 
  ```json
  {
    "course_code": "PHY101",
    "course_name": "Physics I",
    "department": "Computer Engineering",
    "batch": "FYCO",
    "credits": 4
  }
  ```

### Get All Courses
- **GET** `/courses/`

### Get Course by Code
- **GET** `/courses/<course_code>`

### Delete Course
- **DELETE** `/courses/<course_code>`

## Batch Levels
- `FYCO` - First Year Computer Engineering
- `SYCO` - Second Year Computer Engineering  
- `TYCO` - Third Year Computer Engineering

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. API will be available at `http://localhost:5000`

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///courses.db
```
# courses_creation_api
