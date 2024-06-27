from django.contrib import admin
from .models import * 

@admin.register(PartyAccessory, PartyAccessoryImage, PartyAccessoryReview)
class PartyAccessoryAdmin(admin.ModelAdmin):
    def get_model_fields(self, model):
        return [field.name for field in model._meta.fields]

    def get_list_display(self, request):
        model = self.model
        return self.get_model_fields(model)