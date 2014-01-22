
from django.template.defaultfilters import slugify as django_slugify
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from unidecode import unidecode


# Timezone support with fallback.
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


def slugify(s):
    """
    Translates unicode into closest possible ascii chars before
    slugifying.
    """
    return django_slugify(unidecode(unicode(s)))


def unique_slug(manager, slug_field, slug):
    """
    Ensure slug is unique for the given manager, appending a digit
    if it isn't.
    """
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit("-", 1)[0]
            slug = "%s-%s" % (slug, i)
        if not manager.filter(**{slug_field: slug}):
            break
        i += 1
    return slug


def split_choices(choices_string):
    """
    Convert a comma separated choices string to a list.
    """
    return filter(None, [x.strip() for x in choices_string.split(",")])


def import_class(import_path):
        try:
            dot = import_path.rindex('.')
        except ValueError:
            raise ImproperlyConfigured("%s isn't a Python path." % import_path)
        module, classname = import_path[:dot], import_path[dot + 1:]
        try:
            mod = import_module(module)
        except ImportError as e:
            raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                       (module, e))
        try:
            return getattr(mod, classname)
        except AttributeError:
            raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                       'class.' % (module, classname))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip
