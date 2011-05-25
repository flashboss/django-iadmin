import datetime
#import django
#import django.contrib.admin.util
from django.conf import settings
from django.contrib.admin import ModelAdmin as DjangoModelAdmin, TabularInline as DjangoTabularInline, helpers
from django.contrib.admin.util import flatten_fieldsets
from django.db.models.fields import AutoField
from . import widgets
from . import actions as ac
from django.utils.encoding import smart_unicode
from django.utils.http import urlencode
from django.db import models
from django.utils.safestring import mark_safe

__all__ = ['IModelAdmin', 'ITabularInline']

#def empty(modeladmin, request, queryset):
#    modeladmin.model.objects.all().delete()
#empty.short_description = "Empty (flush) the table"


class IModelAdmin(DjangoModelAdmin):
    add_undefined_fields = False
    change_form_template='admin/change_form_tab.html'
    actions = [ac.mass_update, ac.export_to_csv]

    #formfield_overrides = {models.DateField:       {'widget': AdminDateWidget}}

    list_display_rel_links = ()
    cell_filter = ()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        formfield = super(IModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if formfield and db_field.name not in self.raw_id_fields:
            formfield.widget = widgets.RelatedFieldWidgetWrapperLinkTo(formfield.widget, db_field.rel, self.admin_site)
        return formfield

    def _link_to_model(self, obj, label=None):
        if not obj:
            return ''
        url = self.admin_site.reverse_model(obj.__class__, obj.pk)
        return '&nbsp;<span class="linktomodel"><a href="%s"><img src="%siadmin/img/link.png"/></a></span>' % (url, settings.MEDIA_URL)

    def _cell_filter(self, obj, field):
        target = getattr(obj, field.name)
        if not (obj and target):
            return ''
        if isinstance(field.rel, models.ManyToOneRel):
            rel_name = field.rel.get_related_field().name
            lookup_kwarg = '%s__%s__exact' % (field.name, rel_name)
            url = self.get_query_string( {lookup_kwarg: target.pk})
        else:
            lookup_kwarg = '%s__exact' % field.name
            url = self.get_query_string( {lookup_kwarg: target})

        return '&nbsp;<span class="linktomodel"><a href="%s"><img src="%siadmin/img/zoom.png"/></a></span>' % (url, settings.MEDIA_URL)


    def get_query_string(self, new_params=None, remove=None):
        if new_params is None: new_params = {}
        if remove is None: remove = []
        p = dict(self.request.GET.items())
        for r in remove:
            for k in p.keys():
                if k.startswith(r):
                    del p[k]
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                p[k] = v
        return '?%s' % urlencode(p)

    def changelist_view(self, request, extra_context=None):
        self.request =request
        return super(IModelAdmin, self).changelist_view(request, extra_context)

    def _declared_fieldsets(self):
        # overriden to handle `add_undefined_fields`
        if self.fieldsets:
            if self.add_undefined_fields:
                def _valid(field):
                    return field.editable and type(field) not in (AutoField, ) and '_ptr' not in field.name

                flds = list(self.fieldsets)
                fieldset_fields = flatten_fieldsets(self.fieldsets)
                alls = [f.name for f in self.model._meta.fields if _valid(f)]
                missing_fields = [f for f in alls if f not in fieldset_fields ]
                flds.append(('Other', {'fields': missing_fields, 'classes': ('collapse',),},))
                return flds
            else:
                return self.fieldsets
        elif self.fields:
            return [(None, {'fields': self.fields})]
        return None
    declared_fieldsets = property(_declared_fieldsets)


class ITabularInline(DjangoTabularInline):
    template = 'admin/edit_inline/tabular_tab.html'
    add_undefined_fields = False

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        formfield = super(ITabularInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if formfield and db_field.name not in self.raw_id_fields:
            formfield.widget = widgets.RelatedFieldWidgetWrapperLinkTo(formfield.widget, db_field.rel, self.admin_site)
        return formfield


