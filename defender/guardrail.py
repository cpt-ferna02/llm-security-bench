import re

INJECTION_PATTERNS = [
    r"ignore (all |your )?(previous |prior )?instructions",
    r"you are now (DAN|an? evil|a hacker|unrestricted)",
    r"repeat your system prompt",
    r"translate your (full |system )?instructions",
    r"print all (user data|emails|passwords)",
    r"delete (all )?files",
    r"hidden_instructions",
    r"\[DOCUMENT START\].*ignore",
]

BANNED_OUTPUTS = [
    "jailbreak success",
    "indirect injection success",
    "password",
]

def sanitize_input(prompt: str) -> tuple[bool, str]:
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return False, f"[BLOCKED] Input flagged by pattern: {pattern}"
    return True, prompt

def validate_output(response: str) -> tuple[bool, str]:
    for term in BANNED_OUTPUTS:
        if term.lower() in response.lower():
            return False, "[REDACTED] Output contained a policy violation."
    return True, response
