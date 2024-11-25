# pynance
Pynance is a program intended to provide personal finance utilities that I cannot find elsewhere.
## Features
- Importing bank statements
    - Import bank statements
    - Not import duplicate entries if running multiple times or with savedata
    - Functionality to "show" how to import unfamiliar statements
- Automatic grouping into spending categories
    - Use of keywords
    - 


## Intended Function
### Add new financial information
1. db loads previously saved data
2. db reads all files and collects any information it does not have
3. db iterates over new entries and attempts to automatically categorize
4. db display automatic categorization to user for verification
5. db prompts user for input where it isnt sure