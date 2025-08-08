from dataclasses import dataclass, field

SUPPORTED_LANGS = ["it", "en", "fr", "es", "ar", "hi", "ur", "bn", "wo"]


@dataclass
class Context:
    phone: str
    lang: str = "it"
    name: str | None = None
    client_type: str = "new"  # "new" | "active"
    intent: str | None = None
    state: str = "INITIAL"
    stage: str = "DISCOVERY"  # Stage tracking
    asked_name: bool = False  # ← default
    slots: dict[str, str] = field(default_factory=dict)  # generic slot bag
    history: list[dict] = field(default_factory=list)  # last N messages
    rag_chunks: list[str] = field(default_factory=list)  # RAG retrieved chunks
    clarify_count: int = 0  # Counter per loop detection
