from rest_framework.routers import DefaultRouter

from apps.blog.views import BlogPostViewSet, TagViewSet

router = DefaultRouter()
router.register("blog/posts", BlogPostViewSet, basename="blog-post")
router.register("blog/tags", TagViewSet, basename="blog-tag")

urlpatterns = router.urls
