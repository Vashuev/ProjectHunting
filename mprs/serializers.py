from email.policy import default
from rest_framework import serializers
from .models import ProjectModel

class ProjectSerializer(serializers.ModelSerializer):
    votedByMe = serializers.BooleanField(default=True)
    class Meta:
        model = ProjectModel
        fields = ['id', 'logo', 'name', 'subtitle', 
        'description', 'posted_at', 'last_modify',
        'owner_id', 'voteCount', 'url', 'tag', 
        'votedBy','votedByMe'
        ]