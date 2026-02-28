from app.schemas.base import BaseSchema


class ConversationIntelligence(BaseSchema):
    period: str                          
    total_conversations: int
    standard_count: int
    complex_count: int
    standard_pct: float
    complex_pct: float
    clarity_trend: str                   


class TopicBreakdown(BaseSchema):
    topic: str
    count: int
    conversation_type: str               
    pct_of_total: float


class AnalyticsSummary(BaseSchema):
    intelligence: ConversationIntelligence
    top_complex_topics: list[TopicBreakdown]
    top_simple_topics: list[TopicBreakdown]
    suggested_actions: list[str]         