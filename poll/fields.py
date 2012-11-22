import uuid
from django.db import models
from south.modelsinspector import add_introspection_rules

class UUIDField(models.CharField) :
    """
    This great field have been imported from
    http://djangosnippets.org/snippets/1262/
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)

add_introspection_rules([], ["^poll\.fields\.UUIDField"])