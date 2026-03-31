from pydantic import BaseModel, Field

from .boundary_rule import BoundaryRule
from .config_tag_rule import ConfigTagRule
from .flow_rule_set import FlowRuleSet


class RuleSet(BaseModel):
    boundaries: list[BoundaryRule] = Field(default_factory=list)
    tags: list[ConfigTagRule] = Field(default_factory=list)
    flow: FlowRuleSet = Field(default_factory=FlowRuleSet)
