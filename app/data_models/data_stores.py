from dataclasses import dataclass, field
from typing import MutableMapping

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.data_models.supplementary_data_store import SupplementaryDataStore


@dataclass
class DataStores:
    # self.metadata is a read-only view over QuestionnaireStore's self._metadata
    metadata: MetadataProxy | None = None
    response_metadata: MutableMapping = field(default_factory=dict)
    list_store: ListStore = field(default_factory=ListStore)
    answer_store: AnswerStore = field(default_factory=AnswerStore)
    progress_store: ProgressStore = field(default_factory=ProgressStore)
    supplementary_data_store: SupplementaryDataStore = field(
        default_factory=SupplementaryDataStore
    )
