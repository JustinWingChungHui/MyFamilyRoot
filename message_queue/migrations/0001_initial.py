# Generated by Django 2.2.6 on 2019-10-04 10:22

from django.db import migrations, models
import django.db.models.deletion

def create_tag_resize(apps, schema_editor):
    Queue = apps.get_model("message_queue", "Queue")
    resize_tag_queue = Queue(name = "resize_tag",
                    description = """
                    Queue to place tag ids that need to be resized using AI facial recognition
                    integer_data represents the tag id
                    """)
    resize_tag_queue.save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processed', models.BooleanField(default=False)),
                ('string_data', models.CharField(blank=True, max_length=512, null=True)),
                ('integer_data', models.IntegerField(null=True)),
                ('float_data', models.FloatField(null=True)),
                ('date_data', models.DateTimeField(null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message_queue.Queue')),
            ],
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['processed'], name='message_que_process_4ba69b_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['creation_date'], name='message_que_creatio_a7dfb1_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['queue'], name='message_que_queue_i_b6105c_idx'),
        ),
        migrations.RunPython(create_tag_resize),
    ]
