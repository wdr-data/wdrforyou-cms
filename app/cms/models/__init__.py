from .report import *

from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

EmojiPickerTextInput.Media.js = ('admin/js/jquery.init.js', ) + EmojiPickerTextInput.Media.js
EmojiPickerTextarea.Media.js = ('admin/js/jquery.init.js', ) + EmojiPickerTextarea.Media.js
