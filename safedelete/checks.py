from django.core.checks import Tags, register, Warning
from django.contrib import admin

from .config import FIELD_NAME
from .admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted, list_display_deleted_field


@register(Tags.admin)
def check_safe_delete_admin(app_configs=None, **kwargs):
    """
    Checks all registered ModelAdmin classes that subclass ``SafeDeleteAdmin`` for common misconfigurations
    """
    errors = []

    for model, admin_instance in admin.site._registry.items():
        if not isinstance(admin_instance, SafeDeleteAdmin):
            continue

        # Make sure deleted rows are highlighted in at least one way
        if list_display_deleted_field not in admin_instance.list_display and highlight_deleted not in admin_instance.list_display:
            errors.append(
                Warning(
                    msg="ModelAdmin list_display does not include list_display_deleted_field or highlight_deleted, deleted objects will not be highlighted",
                    hint="Add the SafeDeleteAdmin list_display to your ModelAdmin, e.g.: `list_display = (..., ) + SafeDeleteAdmin.list_display`",
                    obj=admin_instance,
                    id="safedelete.W001",
                )
            )
        
        # Make sure deleted items can be filtered
        if SafeDeleteAdminFilter not in admin_instance.list_filter and FIELD_NAME not in admin_instance.list_filter:
            errors.append(
                Warning(
                    msg="ModelAdmin list_filter does not include SafeDeleteAdminFilter, deleted objects will always be shown",
                    hint="Add SafeDeleteAdminFilter to your list_filter, e.g.: `list_filter = (..., SafeDeleteAdminFilter)",
                    obj=admin_instance,
                    id="safedelete.W002",
                )
            )

    return errors
