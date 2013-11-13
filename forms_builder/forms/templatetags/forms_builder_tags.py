from django import template
from django.template.loader import get_template
from forms_builder.forms import settings
from forms_builder.forms.settings import FORM_FOR_FORM
from forms_builder.forms.utils import import_class
from forms_builder.forms.models import Form, FormEntry

register = template.Library()

FormForForm = import_class(FORM_FOR_FORM)


class BuiltFormNode(template.Node):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        request = context["request"]
        user = getattr(request, "user", None)
        post = getattr(request, "POST", None)
        files = getattr(request, "FILES", None)
        context["main_logo"] = settings.MAIN_LOGO
        if self.name != "form":
            lookup = {
                str(self.name): template.Variable(self.value).resolve(context)
            }
            try:
                form = Form.objects.published(for_user=user).get(**lookup)
            except Form.DoesNotExist:
                form = None
        else:
            form = template.Variable(self.value).resolve(context)
        if not isinstance(form, Form) or (form.login_required and not
                                          user.is_authenticated()):
            return ""
        t = get_template("forms/includes/built_form.html")
        context["form"] = form
        form_args = (form, context, post or None, files or None)
        context["form_for_form"] = FormForForm(*form_args)
        return t.render(context)


class BuiltDataFormNode(template.Node):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        form_entry = template.Variable(self.value).resolve(context)

        fields = form_entry.form.fields.order_by('order')
        fields_entry = form_entry.fields.order_by('order')

        data_form_entry = []
        for i in range(fields_entry.count()):
            data = [fields.get(id=fields_entry[i].field_id).label, fields_entry[i].value]
            data_form_entry.append(data)

        t = get_template("forms/includes/built_data_form.html")
        context["data_form_entry"] = data_form_entry
        return t.render(context)


class BuiltDataFormByTemplateNode(template.Node):

    def __init__(self, name, value, template):
        self.name = name
        self.value = value
        self.template = template

    def render(self, context):
        form_entry = template.Variable(self.value).resolve(context)

        fields = form_entry.form.fields.order_by('order').exclude(slug='agree_to_receive_news')
        fields_slug = fields.values('slug')
        fields_entry = form_entry.fields.order_by('order')
        fields_entry_id = [item['field_id'] for item in fields_entry.values('field_id')]

        for i in range(len(fields_entry)):
            slug = fields_slug[i]['slug']
            field_id = fields.get(slug=slug).id
            if field_id in fields_entry_id:
                context[slug] = fields_entry.get(field_id=field_id).value

        t = get_template("forms/includes/%s" % (self.template or form_entry.form.slug + '.html'))
        return t.render(context)


class ContactDataFormNode(template.Node):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        form_entry = template.Variable(self.value).resolve(context)
        slugs = ['fio', 'telefon', 'elektronnaia_pochta']

        fields = form_entry.form.fields.filter(slug__in=slugs)
        fields_id = [field.id for field in fields]
        fields_slugs = [field.slug for field in fields]
        fields_entry = form_entry.fields.filter(field_id__in=fields_id)

        for i in range(len(fields_slugs)):
            slug = fields_slugs[i]
            context[slug] = fields_entry.get(field_id=fields.get(slug=slug).id).value

        t = get_template("forms/includes/contact_data_form.html")
        return t.render(context)


@register.tag
def render_built_form(parser, token):
    """
    render_build_form takes one argument in one of the following formats:

    {% render_build_form form_instance %}
    {% render_build_form form=form_instance %}
    {% render_build_form id=form_instance.id %}
    {% render_build_form slug=form_instance.slug %}

    """
    try:
        _, arg = token.split_contents()
        if "=" not in arg:
            arg = "form=" + arg
        name, value = arg.split("=", 1)
        if name not in ("form", "id", "slug"):
            raise ValueError
    except ValueError:
        e = ()
        raise template.TemplateSyntaxError(render_built_form.__doc__)
    return BuiltFormNode(name, value)


@register.tag
def render_built_data_form(parser, token):
    _, arg = token.split_contents()
    if "=" not in arg:
        arg = "form=" + arg
    name, value = arg.split("=", 1)
    return BuiltDataFormNode(name, value)


@register.tag
def render_contact_data_form(parser, token):
    _, arg = token.split_contents()
    if "=" not in arg:
        arg = "form=" + arg
    name, value = arg.split("=", 1)
    return ContactDataFormNode(name, value)


@register.tag
def render_built_data_form_by_template(parser, token):
    try:
        _, arg, template = token.split_contents()
    except ValueError:
        _, arg = token.split_contents()
        template = None

    if "=" not in arg:
        arg = "form=" + arg
    name, value = arg.split("=", 1)
    return BuiltDataFormByTemplateNode(name, value, template)
