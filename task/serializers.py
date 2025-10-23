from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.username", read_only=True)
    assignees_names = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "creator",
            "creator_name",
            "assignees",
            "assignees_names",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["creator", "created_at", "updated_at"]

    def get_assignees_names(self, obj):
        return [u.username for u in obj.assignees.all()]

    def create(self, validated_data):
        # مدیر به طور خودکار به عنوان creator ذخیره می‌شود
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["creator"] = request.user
        return super().create(validated_data)
