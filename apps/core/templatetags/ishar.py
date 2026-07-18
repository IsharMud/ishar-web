"""
Shared template tags for the Ishar design system (enabler E2).

`{% load ishar %}` then:

    {% bi "rocket-takeoff" %}                        icon via the SVG sprite
    {% bi "lock-fill" css="text-warning" label="Private" %}
    {% crumb "Portal" "person-gear" urlname="portal" anchor="portal" %}
    {% crumb "Deploy" "rocket-takeoff" urlname="deploy" anchor="deploy" active=True %}

Keep these tags tiny and presentation-only; anything data-driven (status maps,
labels) belongs on the model. See docs/design/components.md.
"""
from django import template
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def bi(name, css="", label=""):
    """A Bootstrap Icons sprite icon.

    Decorative by default (aria-hidden); pass `label` to make it meaningful
    (role=img + aria-label). `css` appends classes to the standard `bi`.
    """
    classes = f"bi {css}".strip()
    href = f"{static('bootstrap-icons/bootstrap-icons.svg')}#{name}"
    if label:
        return format_html(
            '<svg class="{}" role="img" aria-label="{}"><use xlink:href="{}"></use></svg>',
            classes, label, href,
        )
    return format_html(
        '<svg class="{}" aria-hidden="true"><use xlink:href="{}"></use></svg>',
        classes, href,
    )


@register.inclusion_tag("partials/crumb.html")
def crumb(label, icon, urlname="", anchor="", active=False, url=""):
    """One breadcrumb item, the site-wide pattern.

    `urlname` is reversed to an href (with `#anchor` appended when given);
    pass a prebuilt `url` instead when the route needs arguments
    (`{% url … as x %}` then `url=x`). Omit both for a plain, unlinked
    crumb. `anchor` also becomes the id of the label span so `focusTo`
    deep-linking keeps working.
    """
    href = url or (reverse(urlname) if urlname else "")
    if href and anchor:
        href = f"{href}#{anchor}"
    return {
        "label": label,
        "icon": icon,
        "href": href,
        "anchor": anchor,
        "active": active,
    }
