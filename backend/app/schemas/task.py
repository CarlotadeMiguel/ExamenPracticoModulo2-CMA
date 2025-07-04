from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.task import Task
from app.extensions import db

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        sqla_session = db.session

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=128),
        error_messages={
            "required": "El título es obligatorio",
            "validator_failed": "Título inválido"
        }
    )
    priority = fields.Str(
        required=True,
        validate=validate.OneOf(["baja", "media", "alta"]),
        error_messages={"validator_failed": "Prioridad inválida"}
    )
