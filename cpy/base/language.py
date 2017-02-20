qualifiers = [
    'const',
    'constexpr',
    'volatile',
]

def validate_qualifier(qualifier):
    assert qualifier in qualifiers