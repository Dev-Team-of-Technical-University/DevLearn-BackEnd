from rest_framework import serializers
from .models import Category, Tag, Course, Lesson

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']



class LessonSerializer(serializers.ModelSerializer):
    video = serializers.FileField(write_only=True, required=True)  # فقط برای دریافت
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'order', 'duration', 'video_url', 'video']

    def create(self, validated_data):
        file = validated_data.pop('video')
        filename = file.name
        video_url = self.upload_to_nextcloud(file, filename)
        lesson = Lesson.objects.create(video_url=video_url, **validated_data)
        return lesson

    def upload_to_nextcloud(self, file_obj, filename):
        import requests

        url = "http://localhost:8000/upload-file"  # آدرس FastAPI شما
        files = {'file': (filename, file_obj.read())}
        data = {'remote_path': f"/videos/{filename}"}

        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            nextcloud_base_url = "http://192.168.1.33:8080/remote.php/dav/files/Meysam08/videos/"
            return nextcloud_base_url + filename
        else:
            raise serializers.ValidationError(f"Video upload failed: {response.text}")



class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.CharField(source='teacher.full_name', read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'teacher', 'teacher_full_name', 'title', 'description', 'category', 'category_title', 'tags', 'thumbnail', 'price', 'is_published', 'created_at']
        read_only_fields = ['id', 'created_at']
