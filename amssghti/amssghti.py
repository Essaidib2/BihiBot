import re
import pywikibot

# Connect to zgh.wikipedia.org
site = pywikibot.Site("zgh", "wikipedia")

# List of specified Tamazight letters
letters = ['ⵣ', 'ⵥ', 'ⵔ', 'ⵕ', 'ⵜ', 'ⵟ', 'ⵢ', 'ⵄ', 'ⵇ', 'ⵙ', 'ⵚ', 'ⴷ', 'ⴹ', 'ⴼ', 'ⴳ', 'ⴳⵯ', 
           'ⵀ', 'ⵃ', 'ⵊ', 'ⴽ', 'ⴽⵯ', 'ⵍ', 'ⵎ', 'ⵡ', 'ⵅ', 'ⵛ', 'ⴱ', 'ⵏ', 'ⵖ']

# Function to remove "ⴻ" except when it's between two identical letters
def remove_e_except_between_identical_letters(text):
    for letter in letters:
        pattern = f'{letter}ⴻ{letter}'
        text = re.sub(pattern, f'{letter}_PLACEHOLDER_{letter}', text)

    text = text.replace("ⴻ", "")
    text = text.replace("_PLACEHOLDER_", "ⴻ")
    return text

# Function to replace hyphen with space except when it is surrounded by spaces
def replace_hyphen(text):
    return re.sub(r"(?<!\s)-(?!\s)", " ", text)

# Function to remove spaces before punctuation marks
def remove_space_before_punctuation(text):
    return re.sub(r'\s+([,.!?;:])', r'\1', text)

# Function to replace specific Tamazight letters with others
def replace_specified_letters(text):
    replacements = {'ⵒ': 'ⴱ', 'ⵞ': 'ⵜⵛ'}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

# Function to reduce multiple spaces between words to one space
def reduce_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

# Function to replace initial "ⵡ" with "ⵓ" if not followed by "ⴰ", "ⵓ", "ⵉ" or if followed by "ⴻ" (removing "ⴻ")
def replace_initial_y(text):
    text = re.sub(r'^ⵡⴻ', 'ⵓ', text)
    return re.sub(r'(^ⵡ(?![ⴰⵓⵉ]))', 'ⵓ', text)
    
# Function to replace initial "ⵢ" with "ⵉ" if not followed by "ⴰ", "ⵓ", "ⵉ" or if followed by "ⴻ" (removing "ⴻ")
def replace_initial_y(text):
    text = re.sub(r'^ⵢⴻ', 'ⵉ', text)
    return re.sub(r'(^ⵢ(?![ⴰⵓⵉ]))', 'ⵉ', text)

# Function to remove any sequence of the vowels "ⴰ", "ⵓ", "ⵉ", "ⴻ" in succession and apply specific replacements
def remove_vowel_sequences(text):
    text = re.sub(r'ⵓⴰ', 'ⵓⵡⴰ', text)
    text = re.sub(r'ⴰⵓ', 'ⴰⵡⵓ', text)
    text = re.sub(r'ⴰⵉ', 'ⴰⵢⵉ', text)
    text = re.sub(r'ⵉⴰ', 'ⵉⵢⴰ', text)
    return re.sub(r'[ⴰⵓⵉⴻ]{2,}', lambda match: match.group(0)[0], text)

# Main function to apply all modifications to a sentence
def apply_modifications(text):
    text = remove_e_except_between_identical_letters(text)
    text = replace_hyphen(text)
    text = remove_space_before_punctuation(text)
    text = replace_specified_letters(text)
    text = replace_initial_y(text)
    text = remove_vowel_sequences(text)
    text = reduce_spaces(text)
    return text

# Function to process all pages in the main namespace on zgh.wikipedia.org
def process_main_namespace():
    modified_pages = 0
    for page in site.allpages(namespace=0):  # Namespace 0 is the main namespace
        try:
            original_text = page.text
            modified_text = apply_modifications(original_text)
            
            if modified_text != original_text:
                page.text = modified_text
                page.save(summary="ⵙⵙⵖⵜⵉⵖ ⴽⵔⴰ ⵏ ⵜⵣⴳⴰⵍ ⵏ ⵓⵙⵏⵎⴰⵔⵔⴰ.")
                print(f"Modified and saved page: {page.title()}")
                modified_pages += 1
            else:
                print(f"No modifications needed for page: {page.title()}")
        except Exception as e:
            print(f"Error processing page {page.title()}: {e}")
    
    print(f"Processing complete. Total modified pages: {modified_pages}")

# Start processing pages
process_main_namespace()
