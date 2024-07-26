from django import template

#

register = template.Library()


@register.inclusion_tag("mobile_notes.html")
def mobile_notes():
    return {}


@register.inclusion_tag("notes/note.html")
def get_note(note):
    return {"note": note}
