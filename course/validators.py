from rest_framework.serializers import ValidationError


class VideoUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = value.get(self.field)

        if tmp_val:
            if 'youtube.com' not in tmp_val:
                raise ValidationError('Можно размещать только ссылки на Youtube')
