from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(name='urlize_post')
def urlize_post(text):
    """
    Convert URLs in text to clickable links.
    Handles both http/https URLs.
    """
    # Pattern to match URLs
    url_pattern = re.compile(
        r'(https?://[^\s]+)',
        re.IGNORECASE
    )
    
    # Replace URLs with HTML links
    def replace_url(match):
        url = match.group(1)
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
    
    text = url_pattern.sub(replace_url, text)
    
    # Keep line breaks
    text = text.replace('\n', '<br>')
    
    return mark_safe(text)
