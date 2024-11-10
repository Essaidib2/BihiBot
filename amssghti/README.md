
# Tamazight Wikipedia Bot Script Overview

## Purpose

This script connects to the Tamazight Wikipedia (zgh.wikipedia.org) and applies various text modifications to all pages in the main namespace. The modifications ensure that the Tamazight text follows specific orthographic and formatting rules.

---

## Script Breakdown

### 1. Connecting to Tamazight Wikipedia

The script uses Pywikibot to connect to `zgh.wikipedia.org`, allowing the bot to access and edit pages within the main namespace (namespace 0).

```python
site = pywikibot.Site("zgh", "wikipedia")
```

### 2. Defining Tamazight Letters

A list of Tamazight letters is defined for use in functions that handle language-specific rules.

```python
letters = ['ⵣ', 'ⵥ', 'ⵔ', 'ⵕ', 'ⵜ', 'ⵟ', 'ⵢ', 'ⵄ', 'ⵇ', 'ⵙ', 'ⵚ', 'ⴷ', 'ⴹ', 'ⴼ', 'ⴳ', 'ⴳⵯ', 
           'ⵀ', 'ⵃ', 'ⵊ', 'ⴽ', 'ⴽⵯ', 'ⵍ', 'ⵎ', 'ⵡ', 'ⵅ', 'ⵛ', 'ⴱ', 'ⵏ', 'ⵖ']
```

### 3. Text Modification Functions

Each function applies a specific rule for handling Tamazight text, addressing character replacements, formatting, and language conventions.

- **`remove_e_except_between_identical_letters`**: Removes "ⴻ" except when it appears between two identical letters, using a placeholder to keep it when necessary.

- **`replace_hyphen`**: Replaces hyphens (`-`) with spaces unless surrounded by spaces to ensure correct spacing.

- **`remove_space_before_punctuation`**: Removes spaces before punctuation marks (`, . ! ? ; :`).

- **`replace_specified_letters`**: Replaces specific letters according to Tamazight rules:
  - "ⵒ" becomes "ⴱ"
  - "ⵞ" becomes "ⵜⵛ"

- **`reduce_spaces`**: Collapses multiple spaces between words into a single space.

- **`replace_initial_w` and `replace_initial_y`**:
  - **`replace_initial_w`**: Replaces initial "ⵡ" with "ⵓ" if not followed by "ⴰ", "ⵓ", or "ⵉ", or if followed by "ⴻ" (removes "ⴻ").
  - **`replace_initial_y`**: Replaces initial "ⵢ" with "ⵉ" under similar conditions.

- **`remove_vowel_sequences`**: Manages sequences of Tamazight vowels ("ⴰ", "ⵓ", "ⵉ", "ⴻ") by making specific replacements (e.g., "ⵓⴰ" → "ⵓⵡⴰ") and reducing long vowel sequences to a single character.

### 4. `apply_modifications` Function

This function chains all text-modification functions to ensure each transformation is applied in sequence.

```python
def apply_modifications(text):
    text = remove_e_except_between_identical_letters(text)
    text = replace_hyphen(text)
    text = remove_space_before_punctuation(text)
    text = replace_specified_letters(text)
    text = replace_initial_y(text)
    text = remove_vowel_sequences(text)
    text = reduce_spaces(text)
    return text
```

### 5. Processing All Pages in the Main Namespace (`process_main_namespace`)

Iterates over all pages in the main namespace, applying the modifications and saving any changes.

- **Page Processing**: 
  - Loads current page text.
  - Applies modifications via `apply_modifications`.
  - Saves the modified text if changes were made, with an edit summary ("ⵙⵙⵖⵜⵉⵖ ⴽⵔⴰ ⵏ ⵜⵣⴳⴰⵍ ⵏ ⵓⵙⵏⵎⴰⵔⵔⴰ") meaning "automatic text correction."
  - Counts and logs modified pages or errors encountered.

```python
def process_main_namespace():
    for page in site.allpages(namespace=0):
        original_text = page.text
        modified_text = apply_modifications(original_text)
        if modified_text != original_text:
            page.text = modified_text
            page.save(summary="ⵙⵙⵖⵜⵉⵖ ⴽⵔⴰ ⵏ ⵜⵣⴳⴰⵍ ⵏ ⵓⵙⵏⵎⴰⵔⵔⴰ.")
```

### 6. Execution

The script is initiated by calling `process_main_namespace()` to start processing pages on Tamazight Wikipedia according to the specified rules.

---

## Summary

This bot script is designed to ensure consistency and accuracy in Tamazight text formatting and orthography across Wikipedia. The functions can be customized or expanded to accommodate additional rules if needed.
