#make sure you have all relevant imports
#do this stuff in your api app

#serializers.py
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


#views.py
from rest_framework import viewsets, status
from rest_framework.response import Response


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer

    def get_queryset(self):
        # Dynamically filter the queryset based on the user's entity_id
        return Property.objects.filter(entity_id=self.request.user.entity_id)
    

    def create(self, request, *args, **kwargs):
        # Explicitly check for 'entity_id' in request data
        if 'entity_id' not in request.data:
            return Response({"error": "'entity_id' is required in the request data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


#urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')

urlpatterns = [
    path('', include(router.urls)),
