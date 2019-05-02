#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#     Copyright (C) 2019 Yavor Konstantinov
#

from stream import streamSource
import sys   # used to exit program when an undesirable state occurs
from tokenType import tokType


class mdTokenizer:
    """Class which tokenizes a markdown file by iterating through it line
    by line"""

    def __init__(self, source):
        # Holds a handle to the source class which restricts access to the

        # source file
        self.src = source
        # The current line of text
        self.text = ""
        # The current character
        self.currChar = ''
        # Current index along the line
        self.currIndex = 0
        # The list of tokens
        self.tokens = []

    def getNext(self):
        """ Return the next character in the current line"""
        self.currIndex += 1
        self.currChar = self.text[self.currIndex]
        return self.currChar

    def peekNext(self):
        """ Return the next character without incrementing the position"""
        return self.text[self.currIndex + 1]

    def skipWhiteSpace(self):
        """Skips all whitespace until the next character is encountered"""
        while(self.currChar == ' '):
            self.getNext()

    def skipWhiteSpaceNewLine(self):
        """Resets the current index and consumes whitespace until an any
        character which is not space is reached"""
        # Reset current index
        self.currIndex = 0
        self.skipWhiteSpace()

    def checkEmptyLine(self):
        """Check if the current line is an empty line"""
        if(self.currChar == '\n' or self.currChar == '\r'):
            return True
        return False

    def addEOL(self):
        """Adds an end of line token to the token list"""
        self.tokens.append({"type": tokType.EOL})

    def getNewLine(self):
        """ Get and set the next line from the source file """
        self.text = self.src.returnLine()
        self.currIndex = 0
        self.currChar = self.text[self.currIndex]

    def eatCharsPlain(self):
        """Consumes characters and returns them to the calling function in the form of
        a string. This function assumes that what is to be consumed is only
        plain characters without any markup. Used for headings"""
        itemText = ""
        print("Here is the start: " + self.currChar)
        while(self.currChar != '\n'):
            print(self.currChar)
            itemText += self.currChar
            self.getNext()
        return itemText

    def eatCharsMarkup(self):
        """Consume characters which are using some type of markup such as * or **"""
        textArr = []
        while(self.currChar != '\n'):
            # Case of bold text like **WORD**
            if(self.currChar == "*" and self.peekNext() == "*"):
                boldText = ""
                # Skip over the following *
                self.getNext()
                self.getNext()
                while(self.currChar != "*"):
                    boldText += self.currChar
                    self.getNext()

                # at this point, currChar is on the first closing *
                # Move to second *
                self.getNext()
                # Now skipped over ** completely
                self.getNext()

                # Add token for bolded text
                textArr.append({
                    "markup": "B",
                    "content": tokType.BOLD
                })

            # Case of italic text like *WORD*
            elif(self.currChar == "*"):
                italicText = ""
                # Skip over to next character
                self.getNext()
                while(self.currChar != "*"):
                    italicText += self.currChar
                    self.getNext()
                # At this point, currChar is on a * so we skip to the next char
                self.getNext()

                # Add token for italic text
                textArr.append({
                    "markup": "I",
                    "content": tokType.ITALIC
                })

            # Default case for plain text
            else:
                plainText = ""
                while self.currChar != '\n' and self.currChar != '*':
                    plainText += self.currChar
                    self.getNext()

                # Add token for plain text
                textArr.append({
                    "markup": "P",
                    "content": tokType.PLAINTEXT
                })

        return textArr

    def tokenizeMarkedHeading(self):
        """Tokenizes a standard markdown heading"""
        headingSize = 1
        headingText = ""

        while(self.getNext() == '#'):
            if headingSize != 6:
                headingSize += 1

        print("Here is the char:" + self.currChar)
        # Skip over intial whitespace
        self.skipWhiteSpace()
        
        print("Here is the char:" + self.currChar)
        # Add contents of heading
        headingText = self.eatCharsPlain()

        # Append to token list
        self.tokens.append(
            {"type": tokType.MHEADING, "size": headingSize, "content": headingText})
        self.addEOL()

    def tokenizeUnmarkedHeading(self):
        """ Tokenize headings which are underlined """
        textContent = ""
        while(self.getNext() != '\n'):
            textContent += self.currChar
        # skip over the next line since it is useless to parse
        src.returnLine()
        self.tokens.append({
            "type": tokType.UHEADING,
            "content": textContent
        })
        self.addEOL()

    def tokenizeText(self):
        """Tokenizes a standard line of text"""
        textContent = self.eatCharsMarkup()
        self.tokens.append({"type": "Text", "content": textContent})
        self.addEOL()


    def tokenizeLink(self):
        """Tokenizes a standard markdown link"""
        linkTitle = ""
        linkPath = ""
        self.skipWhiteSpace()
        self.getNext()
        self.skipWhiteSpace()
        while(self.getNext() != ']'):
            linkTitle += self.currChar

        # Skip over the ] character
        self.getNext()
        self.skipWhiteSpace()
        # Skip over (
        self.getNext()
        self.skipWhiteSpace()
        while(self.getNext() != ')'):
            linkPath += self.currChar

        self.tokens.append(
            {"type": tokType.LINK, "title": linkTitle, "path": linkPath})

    def tokenizeImage(self):
        """ Tokenizes an image link """
        # skip over the ! char which indicates that it is an image
        self.getNext()
        # The image link in standard markdown is just like the standard link
        self.tokenizeLink()

    def tokenizeCheckItem(self):
        """ Tokenize a checklist item of the form:
            - [ ] ITEM """
        status = None
        checkItemContent = ""
        self.skipWhiteSpace()
        # Skip over the -
        self.getNext()
        self.skipWhiteSpace()
        # Skip over [
        self.getNext()

        if(self.currChar == 'x'):
            status = True

        # Skip over ]
        self.getNext()
        self.getNext()
        self.skipWhiteSpace()
        while(self.currChar != '\n'):
            checkItemContent += self.currChar
            self.getNext()

        self.tokens.append(
            {"type": tokType.CHECKMARK, "status": status, "content": checkItemContent})
        self.addEOL()

    def isCheckItemOrBullet(self):
        """Check if the current line is a simple list bullet or is a checkmark"""
        # Used to look ahead in the string
        lookAheadIndex = self.currIndex + 1
        while(lookAheadIndex != len(self.text)):
            if(self.text[lookAheadIndex] == '['):
                return 1
            lookAheadIndex += 1

    def tokenizeBullet(self):
        """ Tokenize a markdown bullet """
        # skip over + or - or *
        self.getNext()
        self.currIndex += 1
        self.skipWhiteSpace()
        text = self.eatCharsMarkup()
        self.tokens.append(
            {"type": tokType.BULLET, "content": text}
        )

    # TODO Check if block is properly formatted
    def tokenizeCodeBlock(self):
        """ Tokenize a code block. """
        tickCount = 0
        lang = ""
        codeBlockContent = []
        while(self.currChar == '`'):
            tickCount += 1
            self.getNext()
        if(tickCount == 3):
            # Consume characters
            lang = self.eatCharsPlain()
            # get next line
            self.getNewLine()
            while self.currChar != '`':
                if self.checkEmptyLine():
                    print("Detected blank line")
                    codeBlockContent.append({
                        "type": "BLANK"
                    })
                    print("Got to here")
                    self.getNewLine()
                else:
                    # Consume entire line
                    lineContent = self.eatCharsPlain()
                    codeBlockContent.append({
                        "line": lineContent
                    })
                    print("Got to else")
                    self.getNewLine()

            tickCount = 0
            while self.currChar == '`':
                tickCount += 1
                self.getNext()

            # Case of malformed block
            if tickCount != 3:
                errString = """Malformed code block ending at line: {}\nMissing {} tickmark""".format(
                    src.getLineNum(), (3 - tickCount))
                sys.exit(errString)

            # At this point, we have a line with the form of ```
            self.tokens.append({
                "type": tokType.CBLOCK,
                "lang": lang,
                "content": codeBlockContent
            })

        else:
            errString = "Error recognizing markdown syntax at line number: {} ".format(
                src.getLineNum)
            sys.exit(errString)

    def returnTokenList(self):
        """ Return the list of tokens """
        return self.tokens

    def tokenize(self):
        """ General driver of the entire tokenizer. 
            It applies the tokenizing rules based on the context detected
            by the first character of the stream which has not yet been consumed """
        while(src.checkEOF()):
            self.getNewLine()
            self.skipWhiteSpaceNewLine()
            # Standard heading starting with #
            if self.currChar == '#':
                print("Tripped test 1")
                self.tokenizeMarkedHeading()
            # Underlined heading
            elif(src.lookAheadLineTest("^(-{2,}|={2,})")):
                print("Tripped test 2")
                self.tokenizeUnmarkedHeading()
            # Either a bullet or checklist item
            elif(self.currChar == '-'):
                print("Tripped test 3")
                if(self.isCheckItemOrBullet() == 1):
                    self.tokenizeCheckItem()
                else:
                    self.tokenizeBullet()
            # Image link
            elif(self.currChar == '!'):
                print("Tripped test 4")
                self.tokenizeImage()
            # Normal link
            elif(self.currChar == '['):
                print("Tripped test 5")
                self.tokenizeLink()
            # Bullet starting with a +
            elif(self.currChar == '+'):
                print("Tripped test 6")
                self.tokenizeBullet()
            # Bullet starting with a *
            elif(self.currChar == '*' and self.peekNext() == " "):
                print("Tripped test 7")
                self.tokenizeBullet()
            elif(self.currChar == '`'):
                print("Tripped test for code block")
                self.tokenizeCodeBlock()
            # Plain sentence
            elif(str.isalnum(self.currChar)):
                print("Tripped test 8")
                self.tokenizeText()
            # Blank line
            elif(self.checkEmptyLine()):
                print("Tripped test BLANK")
                self.tokens.append({"type": tokType.BLANK})
            # Unhandled case
            else:
                pass

        # Add an EOF token
        self.tokens.append({"type": "EOF"})


# temp test
if __name__ == "__main__":
    src = streamSource("test.md")
    tok = mdTokenizer(src)
    tok.tokenize()
    print(tok.returnTokenList())
