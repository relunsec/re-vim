import os
import subprocess
import shutil

VIMRC_PATH = os.path.expanduser("~/.vimrc")
VIM_SYNTAX_PATH = os.path.expanduser("~/.vim/syntax")
AUTOLOAD_DIR = os.path.expanduser("~/.vim/autoload")
PLUG_VIM = os.path.join(AUTOLOAD_DIR, "plug.vim")
BUNDLE_DIR = os.path.expanduser("~/.vim/plugged")
GHIDRA_BRIDGE_DIR = os.path.expanduser("~/.vim/ghidra_bridge")

def install_vim_plug():
    """Install vim-plug plugin manager."""
    if not os.path.exists(PLUG_VIM):
        print("[*] Installing vim-plug...")
        os.makedirs(AUTOLOAD_DIR, exist_ok=True)
        subprocess.run([
            "curl", "-fLo", PLUG_VIM, "--create-dirs",
            "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
        ], check=True)
    else:
        print("[+] vim-plug already installed.")

def install_ghidrabridge():
    """Clone GhidraBridge into a custom directory."""
    if not os.path.exists(GHIDRA_BRIDGE_DIR):
        print("[*] Cloning GhidraBridge...")
        subprocess.run(["git", "clone", "https://github.com/justfoxing/ghidra_bridge.git", GHIDRA_BRIDGE_DIR], check=True)
    else:
        print("[+] GhidraBridge already cloned.")

def write_binwalk_syntax():
    """Create a simple syntax highlighter for binwalk output."""
    os.makedirs(VIM_SYNTAX_PATH, exist_ok=True)
    binwalk_syntax = os.path.join(VIM_SYNTAX_PATH, "binwalk.vim")
    with open(binwalk_syntax, 'w') as f:
        f.write("""
syntax match binwalkOffset /^\\s*\\d\\+/
syntax match binwalkType /\\v(Zip|Linux|ARM|JPEG|Firmware|Executable)/
highlight binwalkOffset ctermfg=Green guifg=Green
highlight binwalkType ctermfg=Yellow guifg=Yellow
""")
    print("[+] Binwalk syntax highlighting created.")

def write_vimrc():
    """Write a .vimrc configured for RE work with all tool integrations."""
    print("[*] Writing .vimrc...")

    vimrc_content = f"""\
" ==============================
" Plugins Setup
" ==============================
call plug#begin('{BUNDLE_DIR}')

Plug 'radareorg/r2.vim'
Plug 'preservim/nerdtree'
Plug 'sheerun/vim-polyglot'
Plug 'vim-airline/vim-airline'
Plug 'preservim/tagbar'

call plug#end()

syntax on
set number
set relativenumber
set tabstop=4 shiftwidth=4 expandtab
set clipboard=unnamedplus
set nowrap
set smartcase
set ignorecase

" Binwalk syntax highlighting
au BufRead,BufNewFile *.binwalk set syntax=binwalk

" NERDTree toggle
nnoremap <C-n> :NERDTreeToggle<CR>

" Tagbar toggle
nnoremap <F8> :TagbarToggle<CR>

" Function: Run GhidraBridge Python script
function! RunGhidraScript(script)
    let l:cmd = 'python3 {GHIDRA_BRIDGE_DIR}/ghidra_bridge.py ' . a:script
    echo "Running Ghidra script: " . a:script
    call system(l:cmd)
endfunction

" Function: Run binwalk on current file and open output in new buffer
function! RunBinwalk()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let l:cmd = 'binwalk --extract --verbose ' . shellescape(expand('%:p'))
    echo "Running binwalk..."
    let l:output = system(l:cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(l:output, '\\n'))
    setlocal nomodifiable
    file BinwalkOutput
endfunction

nnoremap <Leader>b :call RunBinwalk()<CR>

" Function: Run radare2 on current file in a terminal split
function! RunRadare2()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    belowright split | terminal radare2 -AA --colors=on --banner=0 --noprompt --quiet -- '\"' . expand('%:p') . '\"'
    startinsert
endfunction

nnoremap <Leader>r :call RunRadare2()<CR>

" Function: Open a shell terminal split
function! OpenShell()
    belowright split | resize 15 | terminal bash
    startinsert
endfunction

nnoremap <Leader>s :call OpenShell()<CR>

" Function: Run objdump -d on current file and show output in new buffer
function! RunObjdump()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let l:cmd = 'objdump -d ' . shellescape(expand('%:p'))
    echo "Running objdump..."
    let l:output = system(l:cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(l:output, '\\n'))
    setlocal nomodifiable
    file ObjDumpOutput
endfunction

nnoremap <Leader>o :call RunObjdump()<CR>

" Function: Run hexdump -C on current file and show output in new buffer
function! RunHexdump()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let l:cmd = 'hexdump -C ' . shellescape(expand('%:p'))
    echo "Running hexdump..."
    let l:output = system(l:cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(l:output, '\\n'))
    setlocal nomodifiable
    file HexdumpOutput
endfunction

nnoremap <Leader>h :call RunHexdump()<CR>

" Function: Run strings on current file and show output in new buffer
function! RunStrings()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let l:cmd = 'strings ' . shellescape(expand('%:p'))
    echo "Running strings..."
    let l:output = system(l:cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(l:output, '\\n'))
    setlocal nomodifiable
    file StringsOutput
endfunction

nnoremap <Leader>t :call RunStrings()<CR>

" Function: Run gdb on current file in a terminal split
function! RunGdb()
    let filepath = expand('%:p')
    if filepath ==# ''
        echo "No file loaded."
        return
    endif
    if !filereadable(filepath)
        echo "File '" . filepath . "' does not exist."
        return
    endif
    execute 'belowright split | resize 20 | terminal gdb --args ' . shellescape(filepath)
    startinsert
endfunction

nnoremap <Leader>g :call RunGdb()<CR>
" Function: Run strace on current file, output in new buffer
function! RunStrace()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let cmd = 'strace -o /tmp/strace_output.txt ' . shellescape(expand('%:p')) . ' 2>&1'
    echo "Running strace..."
    call system(cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, readfile('/tmp/strace_output.txt'))
    setlocal nomodifiable
    file StraceOutput
endfunction
nnoremap <Leader>x :call RunStrace()<CR>

" Function: Run ltrace on current file, output in new buffer
function! RunLtrace()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let cmd = 'ltrace -o /tmp/ltrace_output.txt ' . shellescape(expand('%:p')) . ' 2>&1'
    echo "Running ltrace..."
    call system(cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, readfile('/tmp/ltrace_output.txt'))
    setlocal nomodifiable
    file LtraceOutput
endfunction
nnoremap <Leader>l :call RunLtrace()<CR>

" Function: Run file command on current file and show output
function! RunFile()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let output = system('file ' . shellescape(expand('%:p')))
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file FileOutput
endfunction
nnoremap <Leader>f :call RunFile()<CR>

" Function: Run strings with address on current file
function! RunStringsExtended()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let cmd = 'strings -a -t x ' . shellescape(expand('%:p'))
    echo "Running extended strings..."
    let output = system(cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file StringsExtendedOutput
endfunction
nnoremap <Leader>e :call RunStringsExtended()<CR>

" Function: Run checksec if available on current file
function! RunChecksec()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    if empty(system('which checksec'))
        echo "checksec not found. Please install it."
        return
    endif
    let cmd = 'checksec --file=' . shellescape(expand('%:p'))
    echo "Running checksec..."
    let output = system(cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file ChecksecOutput
endfunction
nnoremap <Leader>c :call RunChecksec()<CR>

" Function: Run readelf -a on current file
function! RunReadelf()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let cmd = 'readelf -a ' . shellescape(expand('%:p'))
    echo "Running readelf..."
    let output = system(cmd)
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file ReadelfOutput
endfunction
nnoremap <Leader>d :call RunReadelf()<CR>
function! RunRabin2()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let output = system('rabin2 -I ' . shellescape(expand('%:p')))
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file Rabin2Info
endfunction
nnoremap <Leader>i :call RunRabin2()<CR>
function! RunRabin2Sections()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let output = system('rabin2 -S ' . shellescape(expand('%:p')))
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file Rabin2Sections
endfunction
nnoremap <Leader>n :call RunRabin2Sections()<CR>
function! RunCheckELFRelro()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let output = system('readelf -l ' . shellescape(expand('%:p')) . ' | grep GNU_RELRO')
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file RelroCheck
endfunction
nnoremap <Leader>y :call RunCheckELFRelro()<CR>
function! RunLdInfo()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let output = system('ldd ' . shellescape(expand('%:p')))
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file LdInfo
endfunction
nnoremap <Leader>v :call RunLdInfo()<CR>
function! RunElfHeaders()
    if expand('%') == ''
        echo "No file loaded."
        return
    endif
    let output = system('readelf -h ' . shellescape(expand('%:p')))
    new
    setlocal buftype=nofile bufhidden=hide noswapfile
    call setline(1, split(output, '\\n'))
    setlocal nomodifiable
    file ElfHeaders
endfunction
nnoremap <Leader>z :call RunElfHeaders()<CR>



" --- Regexp Search and Highlight ---
function! RegexpSearch()
  let pattern = input('Enter regex pattern: ')
  if empty(pattern)
    echohl ErrorMsg | echo "RegexpSearch: No pattern provided." | echohl None
    return
  endif

  " Clear previous search highlight
  call matchdelete(0)

  " Set search highlighting
  let @/ = pattern
  set hlsearch

  " Move cursor to first match, if any
  if search(pattern) == 0
    echohl WarningMsg | echo "RegexpSearch: No matches found." | echohl None
  else
    echo "RegexpSearch: Matches highlighted."
  endif
endfunction


" Map to <leader>s for quick regex search
nnoremap <leader>s :call RegexpSearch()<CR>

function! OpenCyberChef()
  if has('unix')
    silent execute '!xdg-open https://gchq.github.io/CyberChef/ &'
  elseif has('mac')
    silent execute '!open https://gchq.github.io/CyberChef/ &'
  elseif has('win32') || has('win64')
    silent execute '!start https://gchq.github.io/CyberChef/'
  else
    echo "Unsupported OS for opening web browser"
  endif
  echo "Opening CyberChef in your default browser..."
endfunction
function! Sha256Sum()
  " Get the current file path
  let file = expand('%')

  " Call the sha256sum command with the file and capture the output
  let result = system('sha256sum ' . file)
  
  " Extract just the SHA256 hash from the result
  let hash = split(result)[0]
  
  " Open a new tab and display the hash there in readonly mode
  tabnew
  setlocal readonly          " Make the buffer readonly
  setlocal buftype=nofile    " Set this buffer as a non-file buffer
  " Set the contents of the new tab to the hash
  call setline(1, hash)
endfunction

" Map the leader key + cy to run the Sha256Sum function on the current file
nnoremap <Leader>cy :call Sha256Sum()<CR>


nnoremap <Leader>cy :call OpenCyberChef()<CR>

"""

    with open(VIMRC_PATH, "w") as f:
        f.write(vimrc_content)
    print("[+] .vimrc updated with full RE custom functions.")

def install_plugins():
    """Install Vim plugins using vim-plug."""
    print("[*] Installing Vim plugins...")
    subprocess.run(["vim", "+PlugInstall", "+qall"])

def main():
    if shutil.which("vim") is None:
        print("[!] Vim is not installed. Please install Vim first.")
        return

    install_vim_plug()
    install_ghidrabridge()
    write_binwalk_syntax()
    write_vimrc()
    install_plugins()
    print("[✓] Vim customized for reverse engineering.")

if __name__ == "__main__":
    main()