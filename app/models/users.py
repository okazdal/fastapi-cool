from tortoise import fields, Model


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=50, unique=True, description='Email Address')
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}#{self.username}'


class UserHistory(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    http_url = fields.CharField(max_length=50)
    http_method = fields.CharField(max_length=10)
    request_ip = fields.CharField(max_length=20)
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField('models.User', related_name='events')

    def __str__(self):
        return self.name
