<p align="center">
  <a href="https://github.com/relun">
    <img src="https://avatars.githubusercontent.com/u/213412653?s=200&v=4" alt="Relun Logo" width="150">
  </a>
  <h3 align="center">Relun - Reverse Engineering & Malware Analysis Vim Setup</h3>
  <p align="center">
    Automating your Vim environment for peak reverse engineering productivity.
    <br />
    <a href="#features"><strong>Explore Features »</strong></a>
    ·
    <a href="#installation"><strong>Get Started »</strong></a>
    ·
    <a href="https://github.com/relunsec/re-vim/issues">Report Bug</a>
    ·
    <a href="https://github.com/relunsec/re-vim/issues">Request Feature</a>
  </p>
</p>

---

## ✨ Project Overview: Your Ultimate RE-Vim Setup

Welcome to the **Relun RE-Vim Setup**, a powerful automation script designed to transform your Vim editor into a robust, feature-rich environment specifically tailored for **reverse engineering (RE)** and **malware analysis**. This script streamlines the tedious process of configuring Vim with essential plugins, custom syntax highlighting, and integrated command-line tools, allowing you to focus on the intricate details of binary analysis.

Whether you're examining firmware, dissecting executables, or exploring system calls, this setup provides a unified, efficient workspace right within your favorite text editor.

## 🚀 Features

This script configures Vim with the following powerful capabilities:

* **⚡️ Plugin Management:** Automatically installs **vim-plug**, making it easy to manage your Vim plugins.
* **🔌 Essential RE Plugins:** Includes and configures:
    * **r2.vim:** Seamless integration with **Radare2** for powerful binary analysis.
    * **NERDTree:** A tree explorer plugin for navigating your file system.
    * **vim-polyglot:** Extensive language support for various programming languages.
    * **vim-airline:** A sleek and informative status bar.
    * **Tagbar:** An outline explorer for source code.
* **🌉 GhidraBridge Integration:** Clones and sets up **GhidraBridge**, enabling potential scripting and interaction with Ghidra from within Vim (requires Ghidra and GhidraBridge setup).
* **🌈 Binwalk Syntax Highlighting:** Custom syntax highlighting for `binwalk` output, making it easier to read and analyze firmware/file system extractions.
* **🛠️ Integrated Analysis Tools (Key Mappings):** Access common RE tools directly from Vim:
    * `<Leader>b`: Run **Binwalk** on the current file and open output in a new buffer.
    * `<Leader>r`: Open **Radare2** on the current file in a terminal split.
    * `<Leader>s`: Open a new **Shell terminal** split (for general command execution).
    * `<Leader>o`: Run **Objdump -d** on the current file and show disassembly.
    * `<Leader>h`: Run **Hexdump -C** on the current file for byte-level inspection.
    * `<Leader>t`: Run **Strings** on the current file.
    * `<Leader>g`: Run **GDB** on the current file in a terminal split.
    * `<Leader>x`: Run **Strace** on the current file (output to `/tmp/strace_output.txt` and displayed).
    * `<Leader>l`: Run **Ltrace** on the current file (output to `/tmp/ltrace_output.txt` and displayed).
    * `<Leader>f`: Run **`file`** command on the current file to identify file type.
    * `<Leader>e`: Run **Strings with addresses** (`strings -a -t x`) on the current file.
    * `<Leader>c`: Run **`checksec`** on the current file to analyze security mitigations.
    * `<Leader>d`: Run **`readelf -a`** for full ELF header and section details.
    * `<Leader>i`: Run **`rabin2 -I`** for binary info (Radare2 family).
    * `<Leader>n`: Run **`rabin2 -S`** for section information (Radare2 family).
    * `<Leader>y`: Check for **GNU_RELRO** using `readelf`.
    * `<Leader>v`: Run **`ldd`** to show shared library dependencies.
    * `<Leader>z`: Run **`readelf -h`** for ELF header details.
    * `<Leader>s` (redefined): Interactive **Regexp Search** within the current buffer.
    * `<Leader>cy`: Open **CyberChef** in your default browser.
    * `<Leader>cy` (redefined): Calculate **SHA256Sum** of the current file and display it.

## ⚙️ Installation

To set up your RE-focused Vim environment, simply run the Python script:

1.  **Ensure Vim is installed** on your system.
    ```bash
    # For Debian/Ubuntu
    sudo apt update && sudo apt install vim curl git
    # For Fedora
    sudo dnf install vim curl git
    # For Arch
    sudo pacman -S vim curl git
    ```
2.  **Download the script:**
    ```bash
    git clone [https://github.com/relunsec/re-vim.git](https://github.com/relunsec/re-vim.git)
    cd re-vim
    ```
3.  **Run the script:**
    ```bash
    python3 re_vim.py
    ```

The script will:
* Install `vim-plug`.
* Clone `ghidra_bridge`.
* Create Binwalk syntax highlighting.
* Generate/update your `~/.vimrc` with all the custom functions and key mappings.
* Install all listed Vim plugins.

### Prerequisites

* **Vim:** Your primary editor.
* **Curl:** For downloading `vim-plug`.
* **Git:** For cloning repositories.
* **Python 3:** To run the setup script.
* **Standard RE Tools:** `binwalk`, `radare2`, `objdump`, `hexdump`, `strings`, `gdb`, `strace`, `ltrace`, `file`, `checksec`, `readelf`, `rabin2`, `ldd`. Ensure these are installed and in your system's PATH for the Vim functions to work correctly.

## 🤝 Contributing

We welcome contributions to this Vim setup script! Whether it's adding new tool integrations, improving existing functions, fixing bugs, or enhancing documentation, your help is appreciated.

Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📞 Support & Contact

If you encounter issues or have questions, please open an issue on this repository's [Issues](https://github.com/relunsec/re-vim/issues) page.

For broader inquiries or collaborations with Relun, please refer to our main [organization page](https://github.com/relunsec).

---



---
