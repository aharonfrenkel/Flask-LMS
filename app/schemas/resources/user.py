from app import ma
from app.models import User


class UserPublicSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'email', 'role')