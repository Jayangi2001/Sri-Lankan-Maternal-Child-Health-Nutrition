from typing import TypedDict, Any, List

class MaternalHealthState(TypedDict, total=False):
    user_input: str
    patient_profile: dict
    retrieved_docs: List[str]
    final_response: str
