from tortoise import Model, fields


# Модели для работы с БД
class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.IntField(max_length=50)
    username = fields.CharField(max_length=50)
    full_name = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_manager = fields.BooleanField(default=False)

    class Meta:
        table = "users"

    def __str__(self):
        return f'{self.tg_id} | {self.username}'

    def __repr__(self):
        return self.__str__()


class Notification(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(max_length=50)
    admin_id = fields.IntField(max_length=50)
    text = fields.TextField()
    send_at = fields.DatetimeField(blank=True)
    answer_time = fields.IntField(blank=True)
    is_sent = fields.BooleanField(default=False)
    expired = fields.BooleanField(default=False)

    class Meta:
        table = "notifications"

    def __str__(self):
        return f'{self.send_at}: {self.user} | {self.text}'

    def __repr__(self):
        return self.__str__()
