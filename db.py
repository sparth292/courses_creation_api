#db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from enum import Enum

class BatchLevels(Enum):
    FYCO = "FYCO"
    SYCO = "SYCO" 
    TYCO = "TYCO"

def get_db_connection():
    return psycopg2.connect(
        host="college-attendance-management-system.cnsm4u028xzh.ap-south-1.rds.amazonaws.com",
        database="somaiya_db",
        user="prayagupadhyaya",
        password="Prayag2308",
        port="5432"
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_code VARCHAR(20) PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL,
            department VARCHAR(100) NOT NULL,
            batch VARCHAR(10) NOT NULL CHECK (batch IN ('FYCO', 'SYCO', 'TYCO')),
            credits INTEGER NOT NULL CHECK (credits > 0)
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

class Course:
    def __init__(self, course_code, course_name, department, batch, credits):
        self.course_code = course_code
        self.course_name = course_name
        self.department = department
        self.batch = batch
        self.credits = credits
    
    def to_dict(self):
        return {
            'course_code': self.course_code,
            'course_name': self.course_name,
            'department': self.department,
            'batch': self.batch,
            'credits': self.credits
        }