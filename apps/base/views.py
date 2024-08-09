from rest_framework.views import APIView
from apps.user.services import UserServices


class BaseView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserServices()
