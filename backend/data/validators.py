from .models import SourceRecordResult

def validate_record_result(value: dict) -> SourceRecordResult:
    return SourceRecordResult.model_validate(value)
