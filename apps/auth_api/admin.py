from django.contrib import admin

from apps.auth_api.models import User, Page, Category, Tag


class BlockhainAdmin(admin.ModelAdmin):
    pass


admin.site.register(User)

admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(Page)
# admin.site.register(BlockChain, BlockhainAdmin)
