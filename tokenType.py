from enum import Enum


class tokType(Enum):
    # Heading starting with a #
    MHEADING = 1
    # Underlined heading
    UHEADING = 2
    # Checkmark
    CHECKMARK = 3
    # Regular link(anything but an image link)
    LINK = 5
    # Plain text in a heading. No markup is recognized
    PLAIN = 6
    # Marked up text
    MARKUPTEXT = 7
    # Bullet mark
    BULLET = 8
    # End of line
    EOL = 9
    # End of file
    EOF = 10
    # Code block
    CBLOCK = 11
    # Blank line
    BLANK = 12
    # Italic
    ITALIC = 13
    # Bold
    BOLD = 14
    # Indent
    INDENT = 15
    # Block Quotes
    BLOCKQUOTE = 16
    # Image
    IMAGE = 17
    # Inline Code
    ICODE = 18
    # Horizontal Rule
    HR = 19
    # Numbered bullet
    NUMBULLET = 20
    # Crossed out text
    CROSS = 21
