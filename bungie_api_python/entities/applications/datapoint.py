from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, config
from marshmallow import fields

from ..model_utils import datetime_field_encoder, datetime_field_decoder


@dataclass_json
@dataclass(kw_only=True)
class Datapoint:
    time: datetime = field(
        metadata=config(
            encoder=datetime_field_encoder,
            decoder=datetime_field_decoder,
            mm_field=fields.DateTime(format='iso')
        )
    )
    count: Optional[int] = field(default=None)
