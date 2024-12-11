# constants.py
APP_NAME = "AndroVault"
APP_VERSION = "1.0.0"

"""Application constants and theme configuration."""

# Color scheme
COLORS = {
    'primary': '#2c3e50',      # Dark blue-gray
    'secondary': '#34495e',    # Lighter blue-gray
    'accent': '#3498db',       # Bright blue
    'success': '#2ecc71',      # Green
    'warning': '#f1c40f',      # Yellow
    'error': '#e74c3c',        # Red
    'bg': '#f5f6fa',          # Light background
    'bg_dark': '#dcdde1',     # Darker background
    'text': '#2f3640',        # Dark text
    'text_light': '#f5f6fa',  # Light text
    'border': '#bdc3c7',      # Border color
}

# Padding and margins
PADDING = {
    'small': 5,
    'medium': 10,
    'large': 20
}

# Font configurations
FONTS = {
    'default': ('Segoe UI', 10),
    'heading': ('Segoe UI', 12, 'bold'),
    'small': ('Segoe UI', 9),
    'monospace': ('Consolas', 10)
}

# Window configurations
WINDOW = {
    'min_width': 800,
    'min_height': 600,
    'default_width': 1024,
    'default_height': 768
}

# Message types
MESSAGE_TYPES = {
    'info': {
        'bg': COLORS['accent'],
        'fg': COLORS['text_light']
    },
    'success': {
        'bg': COLORS['success'],
        'fg': COLORS['text_light']
    },
    'warning': {
        'bg': COLORS['warning'],
        'fg': COLORS['text']
    },
    'error': {
        'bg': COLORS['error'],
        'fg': COLORS['text_light']
    }
}

# Button styles
BUTTON_STYLES = {
    'default': {
        'bg': COLORS['secondary'],
        'fg': COLORS['text_light'],
        'padding': PADDING['medium']
    },
    'primary': {
        'bg': COLORS['accent'],
        'fg': COLORS['text_light'],
        'padding': PADDING['medium']
    },
    'danger': {
        'bg': COLORS['error'],
        'fg': COLORS['text_light'],
        'padding': PADDING['medium']
    }
}

FONT_NAME = "Helvetica"
FONT_SIZE = 10

# File Constants
TWO_FA_FILE = "2fa.key"
MASTER_PASSWORD_FILE = "master.hash"
ACCOUNTS_FILE = "accounts.json"

COMPONENT_STYLES = {
    'treeview': {
        'rowheight': 30,
        'font': FONTS['default'],
        'background': COLORS['bg']
    },
    'button': {
        'padding': PADDING['medium'],
        'font': FONTS['default']
    },
    'entry': {
        'padding': PADDING['small'],
        'font': FONTS['default']
    }
}

WIDGET_STYLES = {
    'button': {
        'default': {...},
        'primary': {...},
        'danger': {...}
    },
    'entry': {...},
    'treeview': {...}
}
