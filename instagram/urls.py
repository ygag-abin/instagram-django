from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from post.schema import schema
from post.views import JWTGraphQLView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user', include('user.urls')),
    path('', include('post.urls')),
    # path("graphql",
         # csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    path('graphql/', JWTGraphQLView.as_view(graphiql=True, schema=schema)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
