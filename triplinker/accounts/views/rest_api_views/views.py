from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.TLAccount_frequest import TLAccount
from accounts.serializers import TLAccountDetailSerializer


class TLAccountDetail(APIView):

    def get(self, request, user_id):
        usr = TLAccount.objects.get(id=user_id)
        serializer = TLAccountDetailSerializer(usr)
        return Response(serializer.data)
