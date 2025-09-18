def format_script(script_type, params):
    """
    Utility to format scripts for DAS commands.
    """
    return f"{script_type} {' '.join(params)}\r\n"