"""
UI styles module.
Contains CSS stylesheets for Panel components.
"""

# Stylesheet for the status filter buttons
FILTER_STYLESHEET = """
/* OK Button (2nd child) */
.bk-btn-group .bk-btn:nth-child(2) {
    color: green !important;
    border-color: green !important;
}
.bk-btn-group .bk-btn:nth-child(2).bk-active {
    background-color: green !important;
    color: white !important;
}

/* Error Button (3rd child) */
.bk-btn-group .bk-btn:nth-child(3) {
    color: red !important;
    border-color: red !important;
}
.bk-btn-group .bk-btn:nth-child(3).bk-active {
    background-color: red !important;
    color: white !important;
}
"""
