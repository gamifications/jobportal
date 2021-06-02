import hashlib
from django.template.defaultfilters import register

@register.filter
def gravatar_url(email, size=40):
    # TEMPLATE USE:  {{ email|gravatar_url:150 }}
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
