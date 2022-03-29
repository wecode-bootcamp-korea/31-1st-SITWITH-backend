from django.db    import models
from cores.models import TimestampZone

class User(TimestampZone): 
    username   = models.CharField(max_length=45, unique=True)
    password   = models.CharField(max_length=2000)
    email      = models.EmailField(max_length=100, null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'