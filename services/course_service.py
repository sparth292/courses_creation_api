from marshmallow import Schema, fields, ValidationError
from psycopg2.extras import RealDictCursor
from db import get_db_connection, Course, BatchLevels

class CourseSchema(Schema):
    course_code = fields.Str(required=True, validate=lambda x: len(x) <= 20)
    course_name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    department = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    batch = fields.Str(required=True, validate=lambda x: x in [level.value for level in BatchLevels])
    credits = fields.Int(required=True, validate=lambda x: x > 0)

course_schema = CourseSchema()

class CourseService:
    
    @staticmethod
    def create_course(course_data):
        try:
            validated_data = course_schema.load(course_data)
        except ValidationError as err:
            return {'error': 'Validation failed', 'details': err.messages}, 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT course_code FROM courses WHERE course_code = %s", 
                         (validated_data['course_code'],))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return {'error': 'Course with this code already exists'}, 409
            
            cursor.execute("""
                INSERT INTO courses (course_code, course_name, department, batch, credits)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING course_code, course_name, department, batch, credits
            """, (
                validated_data['course_code'],
                validated_data['course_name'],
                validated_data['department'],
                validated_data['batch'],
                validated_data['credits']
            ))
            
            result = cursor.fetchone()
            conn.commit()
            
            course = Course(*result)
            cursor.close()
            conn.close()
            
            return {'message': 'Course created successfully', 'course': course.to_dict()}, 201
            
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return {'error': 'Failed to create course', 'details': str(e)}, 500
    
    @staticmethod
    def get_all_courses():
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("SELECT * FROM courses ORDER BY course_code")
            results = cursor.fetchall()
            
            courses = [Course(**row).to_dict() for row in results]
            
            cursor.close()
            conn.close()
            
            return {'courses': courses}, 200
            
        except Exception as e:
            return {'error': 'Failed to retrieve courses', 'details': str(e)}, 500
    
    @staticmethod
    def get_course_by_code(course_code):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("SELECT * FROM courses WHERE course_code = %s", (course_code,))
            result = cursor.fetchone()
            
            if not result:
                cursor.close()
                conn.close()
                return {'error': 'Course not found'}, 404
            
            course = Course(**result).to_dict()
            
            cursor.close()
            conn.close()
            
            return {'course': course}, 200
            
        except Exception as e:
            return {'error': 'Failed to retrieve course', 'details': str(e)}, 500
    
    @staticmethod
    def delete_course(course_code):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT course_code FROM courses WHERE course_code = %s", (course_code,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return {'error': 'Course not found'}, 404
            
            cursor.execute("DELETE FROM courses WHERE course_code = %s", (course_code,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return {'message': 'Course deleted successfully'}, 200
            
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return {'error': 'Failed to delete course', 'details': str(e)}, 500
