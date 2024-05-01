from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    """Custom OpenAPI schema generator."""

    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "user",
                "description": "Operations related to user management",
            },
        ]

        return swagger


SchemaView = get_schema_view(
    openapi.Info(
        title="JE Express API",
        default_version="v1",
        description="JE Express API Documentation",
        terms_of_service="https://www.jeexpress.com/policies/terms/",
        contact=openapi.Contact(email="contact@jeexpress.com"),
    ),
    generator_class=CustomOpenAPISchemaGenerator,
    public=True,
    permission_classes=(permissions.AllowAny,),
)
