from dataclasses import dataclass, field
from enum import Enum

class RFCStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"

@dataclass
class RFC:
    id: str
    title: str
    author: str
    status: RFCStatus
    problem: str
    proposal: str
    impact: str
    timeline: str
    reviewers: list = field(default_factory=list)
    approvers: list = field(default_factory=list)

    def to_markdown(self):
        return f"""# RFC-{self.id}: {self.title}

- Author: {self.author}
- Status: {self.status.value}
- Reviewers: {', '.join(self.reviewers)}
- Approvers: {', '.join(self.approvers)}

## Problem
{self.problem}

## Proposal
{self.proposal}

## Impact
{self.impact}

## Timeline
{self.timeline}
"""
