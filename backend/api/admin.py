from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy

from api.models import User,Article,Issue,Reviewer,Announcements

class UserAdmin(admin.ModelAdmin):
    list_display= (
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'last_login'
        
    )

admin.site.register(User,UserAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'submitted_by',
        'unique_id',
        'title',
        'author_name',
        'status',
        'submitted_date',
        'approved_date'
    )
    readonly_fields = ('unique_id', )  # Make unique_id and submited_date read-only
    search_fields = ('title', 'author_name', 'author_email')
    # list_filter = ('status', 'submission_year')

    # Optionally customize the form layout
    fieldsets = (
        (None, {
            'fields': ('submitted_by','unique_id', 'submission_year','author_name', 'author_email', 'author_phone', 'co_authors','title', 'address', 'subject', 'abstract', 'article_pdf','article_doc','article_copyright',  'status', 'submitted_date','approved_date')
        }),
    )


admin.site.register(Article, ArticleAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display=(
        
        'get_article_unique_id',
        'issue_title',
        'vol_no',
        'issue_no',
        'year',
        'month',
        'issued_date',
        'id'
        
    )
#     readonly_fields = ('get_article_unique_id', ) 
    def get_article_unique_id(self, obj):
        return obj.article_id.unique_id

    # Set the column name in the admin list display
    get_article_unique_id.short_description = 'Article Unique ID'
#     fieldsets=(
#         (
#             None,{
#                 'fields':('get_article_unique_id','issue_title','vol_no','issue_no','year','month','issued_date')
#                 }
#         ),
#     )
admin.site.register(Issue,IssueAdmin)

admin.site.register(Reviewer)
admin.site.register(Announcements)