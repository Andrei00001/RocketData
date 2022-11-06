from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy
from nested_inline.admin import NestedModelAdmin

from app import models
from app.tasks import sync_bods3

register_admin = admin.site.register


class EnterpriseTypeAdmin(admin.ModelAdmin):
    model = models.EnterpriseType
    ordering = ['id']
    list_display = ['type', ]
    fields = ['type', ]


register_admin(models.EnterpriseType, EnterpriseTypeAdmin)


class ProductsAdmin(admin.ModelAdmin):
    model = models.Products
    ordering = ['id']
    list_display = ['name', 'model', 'market_launch_date', ]
    fields = ['name', 'model', 'market_launch_date', ]


register_admin(models.Products, ProductsAdmin)


class EnterpriseEmployeesInline(admin.StackedInline):
    model = models.EnterpriseEmployees
    fields = [
        'user',
    ]
    extra = 1


class EnterpriseProductsInline(admin.StackedInline):
    model = models.EnterpriseProducts
    fields = [
        'products',
    ]
    extra = 1


class ProductsInline(admin.StackedInline):
    model = models.SupplyChainProducts
    fields = [
        'products',
    ]
    extra = 1


class EnterpriseContactsInline(admin.StackedInline):
    model = models.EnterpriseContacts
    fields = [
        'email',
        ('country',
         'city',
         'the_outside',
         'house_number',
         )
    ]
    extra = 1


class CityFilter(admin.SimpleListFilter):
    title = 'City'
    parameter_name = 'city'

    enterprises = models.Enterprise.objects.all()
    try:
        cities = set(models.EnterpriseContacts.objects.filter(enterprise__in=enterprises).values_list('city'))
        cities = [city[0] for city in cities]
    except Exception:
        pass

    def lookups(self, request, model_admin):
        for city in self.cities:
            yield city, gettext_lazy(city)

    def queryset(self, request, queryset):
        value = self.value()
        if value not in self.cities:
            return None
        return queryset.filter(contacts__city=value)


class EnterpriseAdmin(NestedModelAdmin):
    change_form_template = 'admin/change_form_button.html'
    model = models.Enterprise
    ordering = "id",
    readonly_fields = 'provider', 'price', 'move_date',
    fields = 'name', 'type', 'provider', 'price', 'move_date',
    list_display = 'name', 'type'
    inlines = [
        EnterpriseContactsInline,
        EnterpriseProductsInline,
        EnterpriseEmployeesInline
    ]
    list_filter = [
        CityFilter,
    ]
    actions = [
        'clear_the_debt'
    ]

    def provider(self, obj):

        provider = obj.recipient.filter(provider__type__id__lt=obj.type.id).last().provider
        if provider.type.id == 1 and obj.type.id == 4:
            return

        return mark_safe(
            f"<a href=http://127.0.0.1:8000/admin/app/enterprise/{provider.id}/change/ >"
            f"{provider}"
            f'</a>'
        )

    def price(self, obj):
        provider = obj.recipient.filter(provider__type__id__lt=obj.type.id).last().provider
        if provider.type.id == 1 and obj.type.id == 4:
            return
        return obj.recipient.filter(provider__type__id__lt=obj.type.id).last().price

    def move_date(self, obj):
        provider = obj.recipient.filter(provider__type__id__lt=obj.type.id).last().provider
        if provider.type.id == 1 and obj.type.id == 4:
            return
        return obj.recipient.filter(provider__type__id__lt=obj.type.id).last().move_date

    @admin.action(description='Сlear the debt')
    def clear_the_debt(self, request, queryset):
        if len(queryset) > 20:
            queryset = [x.pk for x in queryset]
            sync_bods3.apply_async(
                args=(
                    queryset
                ),
                serializer='json',
            )
            return
        for qs in queryset:
            qs = qs.recipient.last()
            qs.price = 0
            qs.save()


register_admin(models.Enterprise, EnterpriseAdmin)


class SupplyChainAdmin(admin.ModelAdmin):
    model = models.SupplyChain
    readonly_fields = 'move_date',
    fields = 'provider', 'recipient', 'price', 'move_date'
    list_display = 'provider', 'recipient', 'price', 'move_date'
    inlines = [
        ProductsInline,
    ]


register_admin(models.SupplyChain, SupplyChainAdmin)
