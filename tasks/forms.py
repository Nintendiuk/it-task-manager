from django.contrib.auth.forms import UserCreationForm
from tasks.models import Position, Worker


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        empty_label="-- No position --",
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = [
            "username", "first_name", "last_name",
            "email", "position", "password1", "password2",
        ]
