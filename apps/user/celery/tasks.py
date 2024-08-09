import pytz

from django.utils import timezone

from config.celery import app

from apps.user.models import CustomUser, BannedIP


@app.task
def clear_banned_until_fields():
    try:
        CustomUser.objects.filter(
            banned_until__isnull=False,
            banned_until__lte=timezone.now().astimezone(pytz.UTC)
        ).update(banned_until=None)
        print("user done")

        BannedIP.objects.filter(
            banned_until__isnull=False,
            banned_until__lte=timezone.now().astimezone(pytz.UTC)
        ).delete()
        print("ips done")

    except Exception as e:
        raise str(e)
