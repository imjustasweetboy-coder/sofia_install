===============================================================================
  SOFIA — Local LLM Harness
  Developed by MENOS RUIDO (https://menosruido.store)
===============================================================================

ABOUT SOFIA
-----------
SOFIA is a lightweight, high-performance CLI harness designed to bring local, 
privacy-focused AI code generation and real-time refactoring directly into 
your command-line interface. 

By running fully on your local machine, SOFIA guarantees complete data 
privacy, zero API costs, and seamless integration with any project structure.

FEATURES
--------
- Privacy First: 100% local inference via Ollama. No code leaves your system.
- Autonomous Auto-Correction: Integrates directly with static analysis tools 
  to catch and fix syntax issues before saving changes.
- System Resource Guard: Built-in RAM monitoring to prevent system freezes.
- Zero-Configuration Setup: Automatically checks, launches, and manages 
  background dependencies.

INSTALLATION STEPS
------------------
1. Extract the contents of 'SOFIA_Win_Set_Up.zip'.
2. Run 'SOFIA_Installer.exe'.
3. If Windows SmartScreen displays a warning:
   - Click "More info".
   - Click "Run anyway".
4. Follow the setup wizard to complete installation. The installer will 
   automatically add SOFIA to your System PATH (`C:\Tools`).
5. Open a new terminal window to apply environment changes.

QUICK START & USAGE
-------------------
Run SOFIA from any terminal (CMD, PowerShell, or integrated IDE terminal) 
using the global `sofia` command:

  sofia -i "<INSTRUCTION>" -f "<TARGET_FILE_PATH>"

EXAMPLES
--------
1. Create a new module or script:
   sofia -i "Create an isolated HTTP service class" -f "lib/services/api_service.dart"

2. Modify or refactor existing code:
   sofia -i "Refactor this widget to use Provider for state management" -f "lib/main.dart"

3. Get command-line help:
   sofia --help

COMMAND-LINE ARGUMENTS
----------------------
  -i, --instruction   Specifies the prompt or code modification instruction.
  -f, --file          Path to the target file to create or modify.

SYSTEM REQUIREMENTS
-------------------
- Operating System: Windows 10/11 (64-bit)
- Memory: 8 GB RAM minimum (16 GB recommended for smooth inference)
- Disk Space: ~5 GB free space for local model weights
- Internet Connection: Required only during initial launch to pull model weights

TERMS OF USE & DISCLAIMER
-------------------------
- License: Proprietary Software licensed under the MENOS RUIDO End User 
  License Agreement. See LICENSE.txt for full terms.
- Liability: SOFIA modifies local files based on AI inference outputs. 
  Always use version control (e.g., Git) to track changes before executing 
  modifications. MENOS RUIDO is not liable for data loss or unintended file edits.

===============================================================================
Support, License Inquiries & Updates: https://menosruido.store
Copyright (c) 2026 MENOS RUIDO. All rights reserved.
===============================================================================
