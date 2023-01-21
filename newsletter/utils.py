import random
import string

def generate_slug(instance):
    chars = string.ascii_letters + string.digits
    new_slug = "".join(random.choice(chars) for _ in range(30))
    klass = instance.__class__

    slug_already_exists =  klass.objects.filter(slug = new_slug).exists()
    if slug_already_exists:
        return generate_slug(instance)
    return new_slug