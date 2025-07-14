from rest_framework import serializers
from dashboard_app.models import Board, Task, Comment
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user with full name."""
    
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']

    def get_fullname(self, obj):
        """Return full name of the user."""
        return f'{obj.first_name} {obj.last_name}'.strip()


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task with user info and comment count."""
    
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True, required=True
    )

    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer', write_only=True, required=True
    )

    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(), required=True
    )

    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'created_at']

    def get_comments_count(self, obj):
        """Return number of comments on the task."""
        return obj.comments.count()

    def create(self, validated_data):
        """Set the task creator to the current user."""
      
        request = self.context['request']
        validated_data['creator'] = request.user
        return super().create(validated_data)
    
    def validate_board(self, value):
        try:
            Board.objects.get(id=value.id)
        except Board.DoesNotExist:
            raise NotFound("Board not found.")
        return value


class TaskCommentSerializer(serializers.ModelSerializer):
    """Serializer for a comment with author name."""
    
    user = UserSerializer(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'user', 'task', 'created_at']

    def get_author(self, obj):
        """Return full name of the comment author."""
        return f'{obj.user.first_name} {obj.user.last_name}'.strip()

    def create(self, validated_data):
        """Assign user and task to the new comment."""
        request = self.context['request']
        task = self.context['task']
        return Comment.objects.create(content=validated_data['content'], user=request.user, task=task)


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for board with task stats and members."""

    owner_id = serializers.SerializerMethodField()
    
    tasks = TaskSerializer(many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_id',
            'members',
            'tasks',
        ]
        read_only_fields = ['owner']

    def get_owner_id(self, obj):
        return obj.owner.id

    def validate(self, data):
        """General validation (can be extended)."""
        print("Main validate called with:", data)
        return data

    def validate_members(self, value):
        """Disallow superusers as board members."""
        superusers = [user for user in value if user.is_superuser]
        if superusers:
            raise serializers.ValidationError("Superusers cannot be added as board members.")
        return value

    def to_representation(self, instance):
        """Return nested member data using UserSerializer."""
        rep = super().to_representation(instance)
        members_qs = instance.members.all()
        rep['members'] = UserSerializer(members_qs, many=True).data
        return rep



class BoardListSerializer(serializers.ModelSerializer):
    """Serializer for board with task stats and members."""
    
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True 
    )
    
    class Meta:
        model = Board
        exclude = ['owner']

    def get_owner_id(self, obj):
        return obj.owner.id

    def get_member_count(self, obj):
        """Return number of board members."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return total number of tasks."""
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        """Return number of 'to-do' tasks."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Return number of high priority tasks."""
        return obj.tasks.filter(priority='high').count()

    def validate_members(self, value):
        """Disallow superusers as board members."""
        superusers = [user for user in value if user.is_superuser]
        if superusers:
            raise serializers.ValidationError("Superusers cannot be added as board members.")
        return value



       

