'''
Implementing Markdown

In our product, we allow users to use Markdown syntax to seamlessly 
format their text (e.g. bold, italic, strikethrough, underline). 
For example, typing "_test sentence_" would italicize the string.

We want to implement some of these Markdown features below and convert them 
into HTML tags. We are limiting this to single character Markdown annotations 
(e.g. '_' but not '__'). Tags without a closing counterpart should be 
interpreted as the character itself and not an HTML tag.
'''


# Part 1
# Given a string containing italicized Markdown (i.e. with wrapping '_'),
# implement a function `apply_markdown` that converts the italicized substring
# into valid HTML.

# 'this has nested <i>~italic and strikethrough~</i>'
# 'this has nested _XXX_'

MARKDOWN_CHARS = {
    '_': ['<i>', '</i>'],
    '~': ['<s>', '</s>'],
    '*': ['<b>', '</b>']
}
def apply_markdown(text):
    result, _ = dfs_extract_markdown(text, None)
    return result

def dfs_extract_markdown(text_excerpt, markdown_char=None):
    if not text_excerpt:
        return "", 0
    
    result = ""
    left = 1 if markdown_char else 0
    
    while left < len(text_excerpt):
        current_char = text_excerpt[left]
        if markdown_char and current_char == markdown_char:
            # Found our closing markdown char
            opening_tag, closing_tag = MARKDOWN_CHARS[markdown_char][0], MARKDOWN_CHARS[markdown_char][1]
            return f"{opening_tag}{result}{closing_tag}", left
        elif current_char in MARKDOWN_CHARS and left < len(text_excerpt) - 1:
            # Found nested markdown char, extract it
            inner_text, right = dfs_extract_markdown(text_excerpt[left:], current_char)
            left += right + 1
            result += inner_text
        else:
            # Not a special char, just append to result
            result += current_char
            left += 1

    # Did not find closing markdown_char
    if markdown_char:
        result = text_excerpt[:len(text_excerpt) - 1]
        left -= 2
    
    return result, left


def assert_equals(actual, expected):
    assert expected == actual, f"expected:\n'{expected}'\nbut saw:\n'{actual}'"

def test_italics():
    assert_equals(apply_markdown(""), "")
    assert_equals(apply_markdown("this is a sentence"), "this is a sentence")
    assert_equals(apply_markdown("this is _italicized_"), "this is <i>italicized</i>")
    assert_equals(apply_markdown("italicize whitespace _ _"), "italicize whitespace <i> </i>")
    assert_equals(apply_markdown("_this sentence_ _has_ _a_ lot of _italics_"), "<i>this sentence</i> <i>has</i> <i>a</i> lot of <i>italics</i>")
    assert_equals(apply_markdown("this is just a single _ underscore"), "this is just a single _ underscore")
    assert_equals(apply_markdown("_side by side_ _ italic _"), "<i>side by side</i> <i> italic </i>")
    assert_equals(apply_markdown("_should eager match _ if possible_"), "<i>should eager match </i> if possible_")
    print('test_italics tests passed')

# Part 2
# Given a string containing italicized ('_'), strikethrough ('~'), and 
# bold ('*') Markdown, update the `apply_markdown` function to convert 
# italicized, strikethrough, and bolded substrings into valid HTML.
def test_strikethrough_and_bold():
    assert_equals(apply_markdown("this has ~strikethrough~"), "this has <s>strikethrough</s>")
    assert_equals(apply_markdown("this has *bold*"), "this has <b>bold</b>")
    assert_equals(apply_markdown("this has both _italicized_ and ~strikethrough~ and *bolded*"), "this has both <i>italicized</i> and <s>strikethrough</s> and <b>bolded</b>")
    assert_equals(apply_markdown("this has nested _~italic and strikethrough~_"), "this has nested <i><s>italic and strikethrough</s></i>")
    assert_equals(apply_markdown("this has nested _~*italic and strikethrough and bold*~_"), "this has nested <i><s><b>italic and strikethrough and bold</b></s></i>")
    assert_equals(apply_markdown("_italic_~strikethrough~ side by side"), "<i>italic</i><s>strikethrough</s> side by side")
    assert_equals(apply_markdown("this is just a single ~tilde and a single *asterisk"), "this is just a single ~tilde and a single *asterisk")
    assert_equals(apply_markdown("_this has unmatched ~ and * in the middle_"), "<i>this has unmatched ~ and * in the middle</i>")
    print('test_strikethrough_and_bold tests passed')


print('Running tests...')
test_italics()
test_strikethrough_and_bold()
print('All tests passed!')