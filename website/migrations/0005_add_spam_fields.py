from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_seed_nashville_waste_crisis_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingrequest',
            name='is_spam',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='bookingrequest',
            name='spam_reasons',
            field=models.TextField(blank=True, default=''),
        ),
    ]
