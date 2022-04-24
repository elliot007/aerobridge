# Generated by Django 4.0.4 on 2022-04-24 22:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', models.URLField(help_text='URL location of the file')),
                ('name', models.CharField(default='Uploaded File', help_text='Give name to this file e.g. Flight Log from Operation A on 21st Aug.', max_length=140)),
                ('upload_type', models.CharField(choices=[('logs', 'Logs'), ('documents', 'Documents'), ('other', 'Other')], default='other', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlightLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('raw_log', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_submitted', models.BooleanField(default=False)),
                ('is_editable', models.BooleanField(default=True, help_text='Set whether the flight log can be edited. Once the flight log has been signed raw flight log cannot be edited.')),
            ],
        ),
        migrations.CreateModel(
            name='FlightOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Medicine Delivery Operation', help_text='Give a friendly name for this operation', max_length=140)),
                ('type_of_operation', models.IntegerField(choices=[(0, 'VLOS'), (1, 'BVLOS')], default=0, help_text='At the moment, only VLOS and BVLOS operations are supported, for other types of operations, please issue a pull-request')),
                ('is_editable', models.BooleanField(default=True, help_text='Set whether the flight operation can be edited. Once the flight log has been signed a flight operation cannot be edited.')),
                ('start_datetime', models.DateTimeField(default=django.utils.timezone.now, help_text='Specify Flight start date and time in Indian Standard Time (IST)')),
                ('end_datetime', models.DateTimeField(default=django.utils.timezone.now, help_text='Specify Flight end date and time in Indian Standard Time (IST)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('drone', models.ForeignKey(help_text='Pick the drone that will be used to fly this opreation', on_delete=django.db.models.deletion.CASCADE, to='registry.aircraft')),
            ],
        ),
        migrations.CreateModel(
            name='FlightPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Delivery Plan', help_text='Give this flight plan a friendly name', max_length=140)),
                ('plan_file_json', models.JSONField(default=dict, help_text='Paste the QGCS flight plan JSON, for more information about the Plan File Format see: https://dev.qgroundcontrol.com/master/en/file_formats/plan.html')),
                ('geo_json', models.JSONField(default=dict, help_text='Paste the flight plan as GeoJSON')),
                ('is_editable', models.BooleanField(default=True, help_text='Set whether the flight plan can be edited. Once the flight log has been signed a flight plan cannot be edited.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('prefix', models.CharField(default='', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('aircraft', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Aircraft', to='registry.aircraft')),
            ],
        ),
        migrations.CreateModel(
            name='SignedFlightLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('signed_log', models.TextField(help_text='Flight log signed by the drone private key')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('raw_flight_log', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='raw_flight_log', to='gcs_operations.flightlog')),
            ],
        ),
        migrations.CreateModel(
            name='FlightPermission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.JSONField(default=dict)),
                ('geo_cage', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status_code', models.CharField(choices=[('granted', 'granted'), ('denied', 'denied'), ('pending', 'pending')], default='denied', help_text='Permissions', max_length=20)),
                ('operation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Operation', to='gcs_operations.flightoperation')),
            ],
        ),
        migrations.AddField(
            model_name='flightoperation',
            name='flight_plan',
            field=models.ForeignKey(help_text='Pick a flight plan for this operation', on_delete=django.db.models.deletion.CASCADE, to='gcs_operations.flightplan'),
        ),
        migrations.AddField(
            model_name='flightoperation',
            name='operator',
            field=models.ForeignKey(help_text='Assign a operator for this operaiton', on_delete=django.db.models.deletion.CASCADE, to='registry.operator'),
        ),
        migrations.AddField(
            model_name='flightoperation',
            name='pilot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.pilot'),
        ),
        migrations.AddField(
            model_name='flightoperation',
            name='purpose',
            field=models.ForeignKey(default='7a875ff9-79ee-460e-816f-30360e0ac645', help_text='To add additional categories, please add entries to the Activities table', on_delete=django.db.models.deletion.CASCADE, to='registry.activity'),
        ),
        migrations.AddField(
            model_name='flightlog',
            name='operation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcs_operations.flightoperation'),
        ),
    ]
