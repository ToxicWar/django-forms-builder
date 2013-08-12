
# coding: utf-8
from django.core.exceptions import ImproperlyConfigured
from django import forms
from django.forms.extras import SelectDateWidget
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _

from forms_builder.forms.settings import USE_HTML5, EXTRA_FIELDS

try:
    import crispy_forms
    from crispy_forms.layout import Div, Field
except ImportError:
    crispy_forms = None

# Constants for all available field types.
TEXT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX = 4
CHECKBOX_MULTIPLE = 5
SELECT = 6
SELECT_MULTIPLE = 7
RADIO_MULTIPLE = 8
FILE = 9
DATE = 10
DATE_TIME = 11
HIDDEN = 12
NUMBER = 13
URL = 14
DOB = 15

# Names for all available field types.
NAMES = (
    (TEXT, _("Single line text")),
    (TEXTAREA, _("Multi line text")),
    (EMAIL, _("Email")),
    (NUMBER, _("Number")),
    (URL, _("URL")),
    (CHECKBOX, _("Check box")),
    (CHECKBOX_MULTIPLE, _("Check boxes")),
    (SELECT, _("Drop down")),
    (SELECT_MULTIPLE, _("Multi select")),
    (RADIO_MULTIPLE, _("Radio buttons")),
    (FILE, _("File upload")),
    (DATE, _("Date")),
    (DATE_TIME, _("Date/time")),
    (DOB, _("Date of birth")),
    (HIDDEN, _("Hidden")),
)

# Field classes for all available field types.
CLASSES = {
    TEXT: forms.CharField,
    TEXTAREA: forms.CharField,
    EMAIL: forms.EmailField,
    CHECKBOX: forms.BooleanField,
    CHECKBOX_MULTIPLE: forms.MultipleChoiceField,
    SELECT: forms.ChoiceField,
    SELECT_MULTIPLE: forms.MultipleChoiceField,
    RADIO_MULTIPLE: forms.ChoiceField,
    FILE: forms.FileField,
    DATE: forms.CharField,
    DATE_TIME: forms.DateTimeField,
    DOB: forms.DateField,
    HIDDEN: forms.CharField,
    NUMBER: forms.FloatField,
    URL: forms.URLField,
}

# Widgets for field types where a specialised widget is required.
WIDGETS = {
    TEXTAREA: forms.Textarea,
    CHECKBOX_MULTIPLE: forms.CheckboxSelectMultiple,
    RADIO_MULTIPLE: forms.RadioSelect,
    # DATE: SelectDateWidget,
    DOB: SelectDateWidget,
    HIDDEN: forms.HiddenInput,
}

# Some helper groupings of field types.
CHOICES = (CHECKBOX, SELECT, RADIO_MULTIPLE)
DATES = (DATE, DATE_TIME, DOB)
MULTIPLE = (CHECKBOX_MULTIPLE, SELECT_MULTIPLE)

# HTML5 Widgets
if USE_HTML5:
    html5_field = lambda name, base: type("", (base,), {"input_type": name})
    WIDGETS.update({
        # DATE: html5_field("date", forms.DateInput),
        DATE_TIME: html5_field("datetime", forms.DateTimeInput),
        DOB: html5_field("date", forms.DateInput),
        EMAIL: html5_field("email", forms.TextInput),
        NUMBER: html5_field("number", forms.TextInput),
        URL: html5_field("url", forms.TextInput),
    })

# Add any custom fields defined.
for field_id, field_path, field_name in EXTRA_FIELDS:
    if field_id in CLASSES:
        err = "ID %s for field %s in FORMS_EXTRA_FIELDS already exists"
        raise ImproperlyConfigured(err % (field_id, field_name))
    module_path, member_name = field_path.rsplit(".", 1)
    CLASSES[field_id] = getattr(import_module(module_path), member_name)
    NAMES += ((field_id, _(field_name)),)


if crispy_forms:
    DIVS = {
        'fio': Div(Field('fio', css_class='form__input'), css_class='form__row'),
        'mobilnyi_telefon': Div(Field('mobilnyi_telefon', css_class='form__input'), css_class='form__row'),
        'elektronnaia_pochta': Div(Field('elektronnaia_pochta', css_class='form__input'), css_class='form__row'),
        'avtomobil': Div(Field('avtomobil', css_class='form__input', data_starter='styler'), css_class='form__row'),
        'god_vypuska': Div(Field('god_vypuska', css_class='form__inputs', data_starter='styler'), css_class='form__row'),
        'gosudarstvennyi_registratsionnyi_nomer': Div(Field('gosudarstvennyi_registratsionnyi_nomer', css_class='form__input'), css_class='form__row'),
        'probeg': Div(Field('probeg', css_class='form__input'), css_class='form__row'),
        'prichina_obrashcheniia': Div(Field('prichina_obrashcheniia', css_class='form__inputs', data_starter='styler'), css_class='form__row'),
        'mesto_provedeniia_servisnykh_rabot': Div(Field('mesto_provedeniia_servisnykh_rabot', css_class='form__inputs', data_starter='styler'), css_class='form__row'),
        'zhelaemaia_data': Div(
            Div(
                Field(
                    'zhelaemaia_data',
                    css_class='form__input',
                    data_starter='datepick',
                    data_show_trigger='<span class="btn">Выберите дату<span class="btn__sep"></span><span class="icon icon__calendar"></span></span>',
                    data_show_other_months="true",
                    data_change_month="false",
                    data_show_speed="0",
                    data_popup_container="#div_id_zhelaemaia_data>.controls"
                ),
                css_class='form__inputs form__inputs-date'
            ),
            css_class='form__row'
        ),
        'kommentarii': Div(Field('kommentarii', css_class='form__textarea'), css_class='form__row'),
        'nazvanie_meropriiatiia': Div(Field('nazvanie_meropriiatiia', css_class='form__input'), css_class='form__row'),
        'tema_obrashcheniia': Div(Field('tema_obrashcheniia', css_class='form__inputs', data_starter='styler'), css_class='form__row'),
        'vopros': Div(Field('vopros', css_class='form__textarea'), css_class='form__row'),
        'agent': Div(Field('agent', css_class='form__inputs', data_starter='styler'), css_class='form__row'),
        'avtosalon': Div(Field('avtosalon', css_class='form__inputs', data_starter='styler'), css_class='form__row'),
        'marka_vashego_avtomobilia': Div(Field('marka_vashego_avtomobilia', css_class='form__input'), css_class='form__row'),
        'model_vashego_avtomobilia': Div(Field('model_vashego_avtomobilia', css_class='form__input'), css_class='form__row'),
        'planiruemaia_data_pokupki_sleduiushchego_avtomobilia': Div(Field('planiruemaia_data_pokupki_sleduiushchego_avtomobilia', css_class='form__input'), css_class='form__row'),
        'priobretenie_avtomobilia_v_kredit': Div(Field('priobretenie_avtomobilia_v_kredit', css_class='form__radio'), css_class='form__row'),
        'optsii_i_dop_oborudovanie': Div(Field('optsii_i_dop_oborudovanie', css_class='form__input'), css_class='form__row'),
        'marka_avtomobilia': Div(Field('marka_avtomobilia', css_class='form__input'), css_class='form__row'),
        'model_avtomobilia': Div(Field('model_avtomobilia', css_class='form__input'), css_class='form__row'),
        'tip_kuzova': Div(Field('tip_kuzova', css_class='form__input'), css_class='form__row'),
        'tip_dvigatelia': Div(Field('tip_dvigatelia', css_class='form__input'), css_class='form__row'),
        'rul': Div(Field('rul', css_class='form__radio'), css_class='form__row'),
        'tip_kpp': Div(Field('tip_kpp', css_class='form__radio'), css_class='form__row'),
        'nazvanie_aktsii_po_spets_predlozheniiu': Div(Field('nazvanie_aktsii_po_spets_predlozheniiu', css_class='form__input'), css_class='form__row'),
        'diler': Div(Field('diler', css_class='form__input'), css_class='form__row'),
    }
