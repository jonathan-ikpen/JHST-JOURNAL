from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_fix_aim_scope_bullets'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_heading',
            field=models.CharField(blank=True, default='Publishing Timeline', max_length=100),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat1_days',
            field=models.CharField(blank=True, default='7', max_length=20),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat1_label',
            field=models.CharField(blank=True, default='Submission to first decision', max_length=200),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat1_tooltip',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat2_days',
            field=models.CharField(blank=True, default='82', max_length=20),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat2_label',
            field=models.CharField(blank=True, default='Submission to decision after review', max_length=200),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat2_tooltip',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat3_days',
            field=models.CharField(blank=True, default='201', max_length=20),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat3_label',
            field=models.CharField(blank=True, default='Submission to acceptance', max_length=200),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat3_tooltip',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat4_days',
            field=models.CharField(blank=True, default='2', max_length=20),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat4_label',
            field=models.CharField(blank=True, default='Acceptance to online publication', max_length=200),
        ),
        migrations.AddField(
            model_name='publicationschedulepage',
            name='timeline_stat4_tooltip',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
