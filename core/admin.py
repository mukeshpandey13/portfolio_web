from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db import models
from django.contrib.admin import SimpleListFilter
from .models import *

# Custom Filters
class ActiveFilter(SimpleListFilter):
    title = 'Status'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Active'),
            ('0', 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(is_active=True)
        if self.value() == '0':
            return queryset.filter(is_active=False)

class HasContentFilter(SimpleListFilter):
    title = 'Has Content'
    parameter_name = 'has_content'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

# Base Admin Classes
class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with common functionality"""

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if hasattr(self.model, 'created_at'):
            readonly.append('created_at')
        if hasattr(self.model, 'updated_at'):
            readonly.append('updated_at')
        return readonly

    def get_list_display(self, request):
        display = list(super().get_list_display(request))
        if 'is_active' in [f.name for f in self.model._meta.fields]:
            if 'status_icon' not in display:
                display.append('status_icon')
        return display

    def status_icon(self, obj):
        if hasattr(obj, 'is_active'):
            if obj.is_active:
                return format_html('<span style="color: green; font-size: 16px;">●</span>')
            else:
                return format_html('<span style="color: red; font-size: 16px;">●</span>')
        return '-'
    status_icon.short_description = 'Status'

class SingletonModelAdmin(BaseModelAdmin):
    """Admin for models that should have only one active instance"""

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            self.model.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

# Model Admin Classes
@admin.register(MetaData)
class MetaDataAdmin(SingletonModelAdmin):
    list_display = ('title', 'keywords_preview', 'description_preview', 'has_logo')
    list_filter = (ActiveFilter,)
    search_fields = ('title', 'description', 'keywords')

    fieldsets = (
        ('SEO Information', {
            'fields': ('title', 'description', 'keywords'),
            'description': 'Search Engine Optimization settings for your portfolio'
        }),
        ('Branding', {
            'fields': ('logo_charecter',),
            'description': 'Logo character displayed in the site header'
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

    def keywords_preview(self, obj):
        if obj.keywords:
            truncated = obj.keywords[:50] + '...' if len(obj.keywords) > 50 else obj.keywords
            return format_html('<span title="{}">{}</span>', obj.keywords, truncated)
        return format_html('<span style="color: #999;">No keywords</span>')
    keywords_preview.short_description = 'Keywords'

    def description_preview(self, obj):
        if obj.description:
            truncated = obj.description[:60] + '...' if len(obj.description) > 60 else obj.description
            return format_html('<span title="{}">{}</span>', obj.description, truncated)
        return format_html('<span style="color: #999;">No description</span>')
    description_preview.short_description = 'Description'

    def has_logo(self, obj):
        return format_html('<span style="color: green;">✓</span>') if obj.logo_charecter else format_html('<span style="color: red;">✗</span>')
    has_logo.short_description = 'Logo'

@admin.register(Hero)
class HeroAdmin(SingletonModelAdmin):
    list_display = ('full_name', 'title', 'greeting_preview', 'bio_preview')
    list_filter = (ActiveFilter,)
    search_fields = ('full_name', 'title', 'greeting', 'bio')

    fieldsets = (
        ('Hero Information', {
            'fields': ('greeting', 'full_name', 'title'),
            'description': 'Main hero section content displayed on homepage'
        }),
        ('Biography', {
            'fields': ('bio',),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

    def greeting_preview(self, obj):
        if obj.greeting:
            return format_html('<em>{}</em>', obj.greeting)
        return format_html('<span style="color: #999;">No greeting</span>')
    greeting_preview.short_description = 'Greeting'

    def bio_preview(self, obj):
        if obj.bio:
            truncated = obj.bio[:80] + '...' if len(obj.bio) > 80 else obj.bio
            return format_html('<span title="{}">{}</span>', obj.bio, truncated)
        return format_html('<span style="color: #999;">No bio</span>')
    bio_preview.short_description = 'Biography'

@admin.register(About)
class AboutAdmin(SingletonModelAdmin):
    list_display = ('about_word_count', 'avatar_preview')
    list_filter = (ActiveFilter,)
    search_fields = ('about',)

    fieldsets = (
        ('About Content', {
            'fields': ('about',),
            'classes': ('wide',),
            'description': 'Main about section content'
        }),
        ('Avatar', {
            'fields': ('avatar',),
            'description': 'Profile image for about section'
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

    def about_word_count(self, obj):
        if obj.about:
            word_count = len(obj.about.split())
            preview = obj.about[:100] + '...' if len(obj.about) > 100 else obj.about
            return format_html(
                '<div title="{}"><strong>{} words</strong><br><small>{}</small></div>',
                obj.about, word_count, preview
            )
        return format_html('<span style="color: #999;">No content</span>')
    about_word_count.short_description = 'About Content'

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">',
                obj.avatar
            )
        return format_html('<span style="color: #999;">No avatar</span>')
    avatar_preview.short_description = 'Avatar'

# Improved Skill Management
class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    fields = ('title', 'icon', 'is_active')
    classes = ('collapse',)

@admin.register(SlkillGroup)
class SkillGroupAdmin(BaseModelAdmin):
    list_display = ('title', 'skill_count', 'active_skill_count')
    list_filter = (ActiveFilter,)
    search_fields = ('title',)
    inlines = [SkillInline]

    def skill_count(self, obj):
        total = obj.skill_set.count()
        return format_html('<strong>{}</strong> total', total)
    skill_count.short_description = 'Total Skills'

    def active_skill_count(self, obj):
        active = obj.skill_set.filter(is_active=True).count()
        color = 'green' if active > 0 else 'red'
        return format_html('<span style="color: {};">{} active</span>', color, active)
    active_skill_count.short_description = 'Active Skills'

@admin.register(Skill)
class SkillAdmin(BaseModelAdmin):
    list_display = ('title', 'group', 'icon_preview')
    list_filter = (ActiveFilter, 'group')
    search_fields = ('title',)
    list_select_related = ('group',)

    fieldsets = (
        ('Skill Details', {
            'fields': ('title', 'group')
        }),
        ('Display', {
            'fields': ('icon',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 20px;"></i>', obj.icon)
        return format_html('<span style="color: #999;">No icon</span>')
    icon_preview.short_description = 'Icon'

# Enhanced Project Management
@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ('title', 'image_preview', 'skill_count', 'links_available', 'ordering_index')
    list_editable = ('ordering_index',)
    list_filter = (ActiveFilter,)
    search_fields = ('title', 'description')
    filter_horizontal = ('skill',)
    ordering = ('ordering_index',)

    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description'),
            'classes': ('wide',)
        }),
        ('Media', {
            'fields': ('image',),
            'description': 'Project screenshot or preview image'
        }),
        ('Links', {
            'fields': ('demo_url', 'source_url'),
            'description': 'Live demo and source code links'
        }),
        ('Technologies Used', {
            'fields': ('skill',),
            'description': 'Select the technologies/skills used in this project'
        }),
        ('Display Settings', {
            'fields': ('ordering_index', 'is_active'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;">',
                obj.image
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Preview'

    def skill_count(self, obj):
        count = obj.skill.count()
        return format_html('<span style="background: #e3f2fd; padding: 2px 6px; border-radius: 12px;">{}</span>', count)
    skill_count.short_description = 'Skills'

    def links_available(self, obj):
        links = []
        if obj.demo_url:
            links.append(format_html('<a href="{}" target="_blank" style="color: #1976d2;">Demo</a>', obj.demo_url))
        if obj.source_url:
            links.append(format_html('<a href="{}" target="_blank" style="color: #388e3c;">Source</a>', obj.source_url))
        return format_html(' | '.join(links)) if links else format_html('<span style="color: #999;">No links</span>')
    links_available.short_description = 'Links'

# Education & Achievement Management
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution", "degree", "field_of_study", "duration_display", "order")
    list_editable = ("order",)
    list_filter = ("degree", "currently_studying")
    search_fields = ("institution", "field_of_study", "description")

@admin.register(AchievementCategory)
class AchievementCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "issuer", "date_awarded", "featured", "order")
    list_editable = ("order", "featured")
    list_filter = ("category", "featured")
    search_fields = ("title", "issuer", "description")

# Exprience
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "employment_type", "duration_display", "order")
    list_editable = ("order",)
    list_filter = ("employment_type", "currently_working")
    search_fields = ("company", "role", "description")

# Contact Information Management
class InfoItemInline(admin.StackedInline):
    model = InfoItem
    extra = 0
    fields = ('key', 'value', 'link', 'icon', 'is_active')
    classes = ('collapse',)

class SocialLinkInline(admin.StackedInline):
    model = SocialLink
    extra = 0
    fields = ('title', 'link', 'icon', 'is_active')
    classes = ('collapse',)

@admin.register(GetInTouch)
class GetInTouchAdmin(SingletonModelAdmin):
    list_display = ('title', 'info_summary', 'social_summary')
    list_filter = (ActiveFilter,)
    search_fields = ('title', 'description')

    fieldsets = (
        ('Contact Section Content', {
            'fields': ('title', 'description'),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )
    inlines = [InfoItemInline, SocialLinkInline]

    def info_summary(self, obj):
        total = obj.info_items.count()
        active = obj.info_items.filter(is_active=True).count()
        return format_html(
            '<span style="color: green;">{}</span> / <span style="color: #666;">{}</span> active',
            active, total
        )
    info_summary.short_description = 'Info Items'

    def social_summary(self, obj):
        total = obj.social_links.count()
        active = obj.social_links.filter(is_active=True).count()
        return format_html(
            '<span style="color: green;">{}</span> / <span style="color: #666;">{}</span> active',
            active, total
        )
    social_summary.short_description = 'Social Links'

@admin.register(InfoItem)
class InfoItemAdmin(BaseModelAdmin):
    list_display = ('key', 'value_preview', 'link_preview', 'get_in_touch')
    list_filter = (ActiveFilter, 'get_in_touch')
    search_fields = ('key', 'value')
    list_select_related = ('get_in_touch',)

    fieldsets = (
        ('Information', {
            'fields': ('key', 'value', 'get_in_touch')
        }),
        ('Display Options', {
            'fields': ('link', 'icon'),
            'description': 'Optional link and icon for this info item'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def value_preview(self, obj):
        if obj.value:
            return format_html('<code>{}</code>', obj.value[:40] + '...' if len(obj.value) > 40 else obj.value)
        return format_html('<span style="color: #999;">No value</span>')
    value_preview.short_description = 'Value'

    def link_preview(self, obj):
        if obj.link:
            return format_html(
                '<a href="{}" target="_blank" style="color: #1976d2;">🔗 Open</a>',
                obj.link
            )
        return format_html('<span style="color: #999;">No link</span>')
    link_preview.short_description = 'Link'

@admin.register(SocialLink)
class SocialLinkAdmin(BaseModelAdmin):
    list_display = ('title', 'link_preview', 'icon_preview', 'get_in_touch')
    list_filter = (ActiveFilter, 'get_in_touch')
    search_fields = ('title', 'link')
    list_select_related = ('get_in_touch',)

    fieldsets = (
        ('Social Platform', {
            'fields': ('title', 'link', 'get_in_touch')
        }),
        ('Display', {
            'fields': ('icon',),
            'description': 'Icon class for this social platform'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def link_preview(self, obj):
        if obj.link:
            domain = obj.link.split('/')[2] if '://' in obj.link else obj.link.split('/')[0]
            return format_html(
                '<a href="{}" target="_blank" style="color: #1976d2;">🔗 {}</a>',
                obj.link, domain
            )
        return format_html('<span style="color: #999;">No link</span>')
    link_preview.short_description = 'Platform Link'

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 18px;"></i>', obj.icon)
        return format_html('<span style="color: #999;">No icon</span>')
    icon_preview.short_description = 'Icon'

# Messages (Contact Form Submissions)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message_preview', 'submission_date')
    list_filter = ('created',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created')
    date_hierarchy = 'created'

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message Content', {
            'fields': ('message',),
            'classes': ('wide',)
        }),
        ('Metadata', {
            'fields': ('created',),
            'classes': ('collapse',)
        }),
    )

    def message_preview(self, obj):
        if obj.message:
            lines = obj.message.split('\n')
            preview = lines[0][:60] + '...' if len(lines[0]) > 60 else lines[0]
            line_count = len(lines)
            return format_html(
                '<div title="{}"><strong>{}</strong><br><small>{} line{}</small></div>',
                obj.message, preview, line_count, 's' if line_count != 1 else ''
            )
        return format_html('<span style="color: #999;">No message</span>')
    message_preview.short_description = 'Message'

    def submission_date(self, obj):
        if obj.created:
            return format_html(
                '<span title="{}">{}</span>',
                obj.created.strftime('%Y-%m-%d %H:%M:%S'),
                obj.created.strftime('%b %d, %Y')
            )
        return format_html('<span style="color: #999;">Unknown</span>')
    submission_date.short_description = 'Submitted'

    def has_add_permission(self, request):
        return False

# Sections Management
admin.site.register(Sections)

# Admin Site Customization
admin.site.site_header = "🎨 Portfolio Admin Dashboard"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Your Portfolio Administration Panel"