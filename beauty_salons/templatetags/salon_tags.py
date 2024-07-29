from django import template
from beauty_salons.forms import PhoneForm
#

register = template.Library()


@register.inclusion_tag("mobile_notes.html")
def mobile_notes():
    return {}


@register.inclusion_tag("notes/note.html")
def get_note(note):
    return {"note": note}


@register.simple_tag(name="get_phone_form")
def get_phone_form():
    phone_form = PhoneForm()
    return {"phone_form": phone_form}
