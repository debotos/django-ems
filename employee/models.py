from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A one-to-one relationship. Conceptually, this is similar
    # to a ForeignKey but it will directly return a single object. ex. <Car: Audi>
    # and ForeignKey return a list of object ex. [<Car2: Mazda>]
    designation = models.CharField(max_length=20, null=False, blank=False)
    salary = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-salary',)  # - indicate Decending Order
    # Meta inner class in Django models:

    # This is just a class container with some options (metadata)
    # attached to the model. It defines such things as available
    # permissions, associated database table name, whether the
    # model is abstract or not, singular and plural versions of the name etc.
    # https://docs.djangoproject.com/en/dev/ref/models/options/

    def __str__(self):
        # pylint: disable=E1101
        return self.user.get_full_name()


# The user_is_created function will only be called when an instance of User is saved.
@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    # we are doing this because, we took the User model as our Employee model
    # so if the user updated or new user added over time we need to change the
    # Employee model simultaneously, for this signal and all those thing are using
    if created:
        # pylint: disable=E1101
        # When new User created also create an Employee
        Employee.objects.create(user=instance)
    else:
        # When User updated also update the corresponding Employee
        instance.employee.save()
