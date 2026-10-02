LOW={"take_screenshot","zoom_region","analyze_screen","get_windows","get_cursor_position","get_screen_resolution",
     "browser_get_url","browser_get_title","browser_get_text","browser_get_html","browser_get_page_state"}
MEDIUM={"browser_navigate","browser_back","browser_forward","browser_reload","activate_window","focus_browser",
        "move_mouse","scroll","wait_milliseconds"}
HIGH={"click","double_click","right_click","drag","type_text","press_keys","clipboard_read","clipboard_write"}
CRITICAL={"execute_shell_command","execute_python_code","close_window"}
def classify(tool,args):
    if tool in CRITICAL:return "critical"
    if tool in HIGH:return "high"
    if tool in MEDIUM:return "medium"
    return "low"
