from django.contrib import admin
from .models import LegalCase, LegalClient, LegalTimeEntry

@admin.register(LegalCase)
class LegalCaseAdmin(admin.ModelAdmin):
    list_display = ["title", "case_number", "client_name", "case_type", "status", "created_at"]
    list_filter = ["case_type", "status"]
    search_fields = ["title", "case_number", "client_name"]

@admin.register(LegalClient)
class LegalClientAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "client_type", "company", "created_at"]
    list_filter = ["client_type"]
    search_fields = ["name", "email", "phone"]

@admin.register(LegalTimeEntry)
class LegalTimeEntryAdmin(admin.ModelAdmin):
    list_display = ["case_title", "attorney", "hours", "rate", "amount", "created_at"]
    list_filter = ["activity"]
    search_fields = ["case_title", "attorney"]
