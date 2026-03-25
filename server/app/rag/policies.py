POLICY_DOCS = [
    {
        "id": "policy_close_fri_sat",
        "document": "Friday and Saturday require two closers whenever possible.",
        "metadata": {"category": "coverage", "shift_type": "close"},
    },
    {
        "id": "policy_close_hours",
        "document": "Closing shifts run from 1:15 PM to 9:15 PM.",
        "metadata": {"category": "shift_template", "shift_type": "close"},
    },
    {
        "id": "policy_open_hours",
        "document": "Open shifts run from 9:00 AM to 5:00 PM.",
        "metadata": {"category": "shift_template", "shift_type": "open"},
    },
    {
        "id": "policy_mid_hours_10",
        "document": "One mid shift option runs from 10:00 AM to 6:00 PM.",
        "metadata": {"category": "shift_template", "shift_type": "mid10"},
    },
    {
        "id": "policy_mid_hours_11",
        "document": "One mid shift option runs from 11:00 AM to 7:00 PM.",
        "metadata": {"category": "shift_template", "shift_type": "mid11"},
    },
    {
        "id": "policy_priority_order",
        "document": "When finding coverage, prioritize floaters first, then dedicated employees from the same store, then dedicated employees from another store, and managers as emergency last resort.",
        "metadata": {"category": "ranking"},
    },
    {
        "id": "policy_custom_shifts",
        "document": "Custom shifts are rare and should be treated as manager-approved exceptions.",
        "metadata": {"category": "exceptions"},
    },
]