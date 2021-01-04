" nvim configuration
" by Junyoung Park <junyoung@uxf.ai>

call plug#begin()
Plug 'junegunn/fzf'
Plug 'preservim/nerdtree', { 'on':  'NERDTreeToggle'  }
" vim status bar
Plug 'vim-airline/vim-airline'
Plug 'overcache/NeoSolarized'
call plug#end()

" --- general configuration ---
filetype plugin on
let g:mapleader = "," " set leader key to comma
set number						" line number
set hlsearch					" highlight searching result
set ignorecase				" ignore case sensitive when searching
set showmatch 				" highglight matched bracket ()

" --- indentation ---
set smartindent
set tabstop=2
set shiftwidth=2
set expandtab
set autoindent
set cindent

" --- turn of swap ---
set noswapfile
set nobackup
set nowb

" --- optional ---
set title
set termguicolors
syntax sync minlines=200 " for speed up vim

" --- NeoSolarized ---
colorscheme NeoSolarized
set background=dark

" NERDtree configurations
let g:NERDTreeDirArrowExpandable = '▸'
let g:NERDTreeDirArrowCollapsible = '▾'
let NERDTreeShowHidden=1

" --- key mapping ---
inoremap jk <Esc>				" esc in inser mode
cnoremap jk <C-C>				" esc in command mode
