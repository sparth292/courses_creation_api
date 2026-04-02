import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from db import init_db
from routes.courses_root import courses_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    CORS(app)
    
    init_db()
    
    app.register_blueprint(courses_bp)
    
    @app.route('/')
    def index():
        return {
            'message': 'Course Creation API',
            'version': '1.0.0',
            'database': 'PostgreSQL',
            'endpoints': {
                'create_course': 'POST /courses/create',
                'get_all_courses': 'GET /courses/',
                'get_course': 'GET /courses/<course_code>',
                'delete_course': 'DELETE /courses/<course_code>'
            }
        }
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)