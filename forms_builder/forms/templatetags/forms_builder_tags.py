from django import template
from django.template.loader import get_template
from forms_builder.forms import settings
from forms_builder.forms.forms import FormForForm
from forms_builder.forms.models import Form, FormEntry


register = template.Library()


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

        fields = form_entry.form.fields.all()
        fields_entry = form_entry.fields.all()

        data_form_entry = []
        for i in range(fields_entry.count()):
            data = [fields.get(id=fields_entry[i].field_id).label, fields_entry[i].value]
            data_form_entry.append(data)

        t = get_template("forms/includes/built_data_form.html")
        context["data_form_entry"] = data_form_entry
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
