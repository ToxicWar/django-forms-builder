
from django.conf import settings


# The maximum allowed length for field values.
FIELD_MAX_LENGTH = getattr(settings, "FORMS_BUILDER_FIELD_MAX_LENGTH", 2000)

# The maximum allowed length for field labels.
LABEL_MAX_LENGTH = getattr(settings, "FORMS_BUILDER_LABEL_MAX_LENGTH", 200)

# Sequence of custom fields that will be added to the form field types.
EXTRA_FIELDS = getattr(settings, "FORMS_BUILDER_EXTRA_FIELDS", ())

# The absolute path where files will be uploaded to.
UPLOAD_ROOT = getattr(settings, "FORMS_BUILDER_UPLOAD_ROOT", None)

# Boolean controlling whether HTML5 form fields are used.
USE_HTML5 = getattr(settings, "FORMS_BUILDER_USE_HTML5", True)

SITE_MODEL = getattr(settings, "FORMS_BUILDER_SITE_MODEL", '')

# Boolean controlling whether forms are associated to Django's Sites framework.
USE_SITES = getattr(settings, "FORMS_BUILDER_USE_SITES",
                    "django.contrib.sites" in settings.INSTALLED_APPS or SITE_MODEL)

# Boolean controlling whether form slugs are editable in the admin.
EDITABLE_SLUGS = getattr(settings, "FORMS_BUILDER_EDITABLE_SLUGS", False)

# Char to start a quoted choice with.
CHOICES_QUOTE = getattr(settings, "FORMS_BUILDER_CHOICES_QUOTE", "`")

# Char to end a quoted choice with.
CHOICES_UNQUOTE = getattr(settings, "FORMS_BUILDER_CHOICES_UNQUOTE", "`")

# Char to use as a field delimiter when exporting form responses as CSV.
CSV_DELIMITER = getattr(settings, "FORMS_BUILDER_CSV_DELIMITER", ",")

# Boolean controlling whether emails to staff recipients are sent from the form submitter.
SEND_FROM_SUBMITTER = getattr(settings, "FORMS_BUILDER_SEND_FROM_SUBMITTER", True)

# Logo url
MAIN_LOGO = getattr(settings, "FORMS_BUILDER_MAIN_LOGO", '')

# Main domain
MAIN_DOMAIN = getattr(settings, "MAIN_DOMAIN", '')

# Form FormForForm
FORM_FOR_FORM = getattr(settings, "FORMS_BUILDER_FORM_FOR_FORM", 'forms_builder.forms.forms.FormForForm')
