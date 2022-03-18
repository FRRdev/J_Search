from tortoise import fields, models


class Verification(models.Model):
    """ Модель для подтверждения регистрации пользователя
    """
    link = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='verification')
