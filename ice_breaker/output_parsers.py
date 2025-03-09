from typing import List, Dict, Any

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="Summary")
    facts: List[str] = Field(description="Interesting facts about the person")

    def to_dict(self) -> Dict[str, Any]:
        return {'facts': self.facts, 'summary': self.summary}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
