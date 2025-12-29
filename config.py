"""
Configuration for web automation - centralized selectors and URLs.
"""
LOGIN_CONFIG = {
    "url": "https://the-internet.herokuapp.com/login",
    "username_selector": "#username",
    "password_selector": "#password",
    "submit_selector": "button[type='submit']",
    "success_url_contains": "/secure",
    "error_message_selector": "#flash",
    "username": "tomsmith",
    "password": "SuperSecretPassword!",
    "timeout": 10
}

DOWNLOAD_CONFIG = {
    "url": "https://the-internet.herokuapp.com/download",
    "download_link_selector": "a[href*='.txt']",
    "expected_filename": "*.txt",
    "timeout": 10
}

FORM_CONFIG = {
    "url": "https://the-internet.herokuapp.com/forgot_password",
    "fields": [
        {"name": "email", "selector": "#email", "value": "test@example.com"}
    ],
    "submit_selector": "button[type='submit']",
    "success_selector": "#content",
    "timeout": 10
}

SCRAPE_CONFIG = {
    "url": "https://the-internet.herokuapp.com/tables",
    "table_selector": "#table1",
    "row_selector": "tbody tr",
    "cell_selector": "td",
    "next_button_selector": ".pagination .next",
    "headers": ["Last Name", "First Name", "Email", "Due", "Web Site", "Action"],
    "timeout": 10
}

DYNAMIC_CONFIG = {
    "url": "https://the-internet.herokuapp.com/dynamic_loading/1",
    "trigger_selector": "#start button",
    "dynamic_element_selector": "#finish",
    "timeout": 10
}

