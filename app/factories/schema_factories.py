from app.schemas import UserRegisterSchema, SessionSchema


user_register_schema = UserRegisterSchema()

create_session_schema = SessionSchema(only=('user_id', 'ip_address', 'user_agent'))