let g:html_use_xhtml = 0
let g:html_dynamic_folds = 0
let g:html_no_foldcolumn = 1 
let g:html_use_encoding = 'UTF-8'
let g:html_font = [
            \ 'Sans Serif', 
            \ 'DejaVu Sans Mono', 
            \ 'Consolas', 
            \ 'monospace'
            \ ]
let html_wrong_comments = 1
let g:html_hover_unfold = 1
" might be computationally demanding
let g:xml_syntax_folding = 0 

setl foldmethod=indent shiftwidth=2 tabstop=4 expandtab

if executable('js-beautify')
    setl formatprg=html-beautify
elseif executable('prettier')
    setl formatprg=prettier\ --parser=markdown
endif

if len($BROWSER) == 0
    for i in ['google-chrome-stable', 
            \ 'google-chrome-beta', 
            \ 'google-chrome-unstable', 
            \ 'google-chrome', 
            \ 'chromium', 
            \ 'firefox-developer', 
            \ 'firefox-developer-edition', 
            \ 'firefox']
        if executable(i)
            let $BROWSER = i
            setl makeprg=$BROWSER\ %
            break
        endif
    endfor
endif

if exists(':EmmetInstall')
	EmmetInstall
	imap <buffer> <Tab> <plug>(emmet-expand-abbr)
endif
