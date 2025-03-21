from marshmallow import Schema, fields, validate

class CreateMeetingSchema(Schema):
    summary = fields.String(required=True, validate=validate.Length(min=5, max=100))
    description = fields.String(required=False, validate=validate.Length(min=5, max=500))
    start_time = fields.String(required=True, validate=validate.Length(min=5, max=100))
    end_time= fields.String(required=True, validate=validate.Length(min=5, max=100))
    time_zone= fields.String(required=True, validate=validate.Length(min=5, max=100))
    attendees= fields.List(fields.String(), required=True, validate=validate.Length(min=1))
    video_conference = fields.Boolean(required=True)