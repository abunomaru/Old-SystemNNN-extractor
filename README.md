# Old-SystemNNN-extractor

> **Superseded by [VNTools](https://github.com/abunomaru/VNTools).** VNTools reads `.spt` files directly (no Wine or `gsspt.exe`), extracts choices and speaker names, inserts translations of any length safely, wraps text to the game's text box, and translates with context using Claude, OpenAI, local models or DeepL. This repository is kept for reference.

This Python script is a fix for extracting .spt files from System-NNN VNs. It resolves the issue related to the "###" characters, providing a solution to accurately extract the content. A DeeplAPI MTL tool was also added.

## How to Use:

1. **Run the Application:**
   When you execute the script, it will create several folders required for the operation.

2. **Select an Option:**
   Upon running, the application prompts you to choose between two options: "1" or "2".

3. **Option 1:**
   This option allows you to process the .spt files.

4. **Option 2:**
   Selecting this option processes the files and generates patched scripts.

### Folder Structure: 

- **spt_files:**
  Place your .spt files from the game here. You can add any number of files.

- **scripts_repaired:**
  This folder contains the patched scripts. You can translate these files without any issue. Ensure not to modify the "###" characters.

- **patch:**
  When you select the second option in the program ("2"), this folder will contain the .spt files with the new text.

## DeepL translation (translate_files_deepl.py)

Translates the text files in `scripts_repaired/` and leaves the `###` marker lines alone:

```bash
export DEEPL_API_KEY=your-key        # free keys end in :fx
python translate_files_deepl.py scripts_repaired/ scripts_translated/ --lang EN-US
```

Then copy the translated files back into `scripts_repaired/` and run option 2.

The script sends the key in the `Authorization: DeepL-Auth-Key` header. DeepL has deprecated the old `auth_key` form parameter, which earlier versions of this script used. It translates line by line in batches and sends the previous lines as `context`, and it needs no packages beyond the Python standard library.
