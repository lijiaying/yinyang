solvers = [
]

crash_msgs = [
    "LEAKED",
    "Leaked",
    "Segmentation fault",
    "segmentation fault",
    "segfault",
    "ASSERTION VIOLATION",
    "Assertion failure",
    "Fatal failure",
    "Internal error detected",
    "an invalid model was generated",
    "Failed to verify",
    "failed to verify",
    "ERROR: AddressSanitizer:",
    "invalid expression",
    "(error",
]

ignore_msgs = [
    "Expected result sat but got unsat",
    "Expected result unsat but got sat",
    "Parse Error",
    "Cannot get model",
    "Symbol 'str.to-re' not declared as a variable",
    "Symbol 'str.to.re' not declared as a variable",
    "Unimplemented code encountered",
    '(error "Error in option parsing: sygus inference not supported with incremental solving")'
]
