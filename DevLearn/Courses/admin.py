from django.contrib import admin

from Courses.models import Category, Tag, Lesson, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# class LessonInline(admin.TabularInline):
#     model = Lesson
#     extra = 1
#     fields = ('title', 'video_url', 'order', 'duration')
#     ordering = ('order',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'category', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'tags', 'created_at')
    search_fields = ('title', 'description', 'teacher__username')
    # inlines = [LessonInline]
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('course', 'order')
