from pydantic import BaseModel, Field
from typing import Optional, Literal


class TestCase(BaseModel):
    """Defines the structure for a single test scenario in the matrix."""

    test_id: str = Field(
        description="A unique identifier for the test.", examples=["TC-001-VALID"]
    )

    # Enforces the scenario must be one of these three exact strings
    scenario_type: Literal["valid", "invalid", "adversarial"]

    user_input: str = Field(description="The simulated prompt from the user")

    expected_tool_call: bool = Field(
        description="Should the agent call the issue_refund tool?"
    )

    # Optional because if expected_tool_call is False, there is no expected ID or amount
    expected_order_id: Optional[str] = Field(
        default=None,
        description="The expected order ID if the tool is called",
        examples=["A1B2", "C3D4"],
    )

    expected_amount: Optional[float] = Field(
        default=None, description="The expected refund amount if the tool is called"
    )

class RefundArguments(BaseModel):
    """The arguments required to execute the issue_refund tool."""
    
    order_id: str = Field(
        description="The alphanumeric identifier for the customer's order.",
        examples=["A1B2", "C3D4"]
    )
    
    amount: float = Field(
        description="The exact refund amount requested in USD. Must be a float.",
    )

if __name__ == "__main__":
    print(RefundArguments.model_json_schema())
