
from __future__ import absolute_import, division, print_function

# Standard Library
from subprocess import run

# 3rd Party
# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import Command


class git(Command):
    """git <subcommand> [<option>, ...] [--] [<file>, ...]

    Wrapper for git commands. Good completion.
    """
    def execute(self):
        command = ['git', '--paginate']

        command.extend(self.args[1:])

        if len(self.fm.thistab.get_selection()) > 1:
            command.append('--')
            command.extend((i.path for i in self.fm.thistab.get_selection()))

        run(command)

        self.fm.ui.need_redraw = True
        self.fm.ui.redraw_main_column()


    def tab(self, tabnum):

        opts = {'--no-pager', '-C'}
        commands = {
            'add',
            'am',
            'apply',
            'archive',
            'bisect',
            'blame',
            'branch',
            'cat-file',
            'checkout',
            'checkout-index',
            'cherry',
            'clean',
            'clone',
            'commit',
            'commit-tree',
            'count-objects',
            'diff',
            'diff-files',
            'diff-index',
            'diff-tree',
            'fast-export',
            'fetch',
            'filter-branch',
            'for-each-ref',
            'for-ls-tree',
            'grep',
            'hash-object',
            'help',
            'index-pack',
            'init',
            'log',
            'ls-files',
            'merge',
            'merge-file',
            'merge-index',
            'mktag',
            'mktree',
            'mv',
            'name-rev',
            'pack-redundant',
            'prune-packed',
            'pull',
            'push'
            'read-tree',
            'rebase',
            'reflog',
            'remote',
            'repack',
            'reset',
            'rev-list',
            'rm',
            'show',
            'show-branches',
            'status',
            'symbolic-ref',
            'tag',
            'unpack-file',
            'update-ref',
            'var',
            'verify-pack',
            'worktree',
            'write-tree',
        }

        return {(" ".join(self.args[:-1]) + " " + i).strip()
                for i in commands if self.args[-1] in i or i in self.args[-1]
                } if len(self.args) > 1 else {f"git {i}" for i in opts}


class vim(Command):
    """:vim [<option>, ...] [<filename>, ...]
    Open marked files in vim.

    NOTE marking only works for the current directory.
    """

    def execute(self):
        command = ['vim'] + self.args[1:]
        command.append('--')
        command.extend(map(lambda x: x.path, self.fm.thistab.get_selection()))
        run(command)
        self.fm.ui.need_redraw = True
        self.fm.ui.redraw_main_column()

    def tab(self, tabnum):

        from os import listdir

        opts = {'-t', '+', '-S', '--cmd', '-d', '-M', '-m', '-o', '-O', '-p', '-R'}

        return {(" ".join(self.args[:-1]) + " " + i).strip()
                for i in opts | set(listdir(self.fm.thisdir.path))
                if self.args[-1] in i or i in self.args[-1]
                } if len(self.args) > 1 else {f"vim {i}" for i in opts}


class grep(Command):
    """:grep <string>

    Looks for a string in all marked files or directories.

    Ripgrep will be attempted before ranger will fallback on git grep and grep.
    """

    def execute(self):
        from subprocess import PIPE
        from os.path import exists, expanduser

        if self.rest(1):

            # try ripgrep
            if exists(expanduser('~/.cargo/bin/rg')):

                x = run([
                    'rg', '--pretty', '--smart-case', '--threads', '16',
                    '--after-context', '1', '--before-context', '1', '--regexp'
                ] + self.args[1:],
                        stdout=PIPE)

            # try git grep if in a git repo
            elif exists(run(['git', 'rev-parse', '--show-toplevel'], PIPE).stdout.decode('utf-8')):

                x = run([
                    'git', 'grep', '--line-number', '--color=always', '-I',
                    '--after-context=3', '--threads=16', '--extended-regexp',
                    '--heading', '--break', '-e'
                ] + self.args[1:],
                        stdout=PIPE)

            # fallback on grep
            else:
                x = run([
                    'grep', '--line-number', '--extended-regexp',
                    '--color=always', '--with-filename', '-r', '-e'
                ] + self.args[1:])

            run(['less', '-R', '-X', '-I'], input=x.stdout)

            self.fm.ui.need_redraw = True
            self.fm.ui.redraw_main_column()


class untracked(Command):
    """:untracked

    List files not tracked by git (ignored).

    Same as git --paginate ls-files --others
    """

    def execute(self):
        run(['git', '--paginate', 'ls-files', '--others'])

        self.fm.ui.need_redraw = True
        self.fm.ui.redraw_main_column()


class tracked(Command):
    """:tracked

    List files tracked by git.

    Same as git --paginate ls-files
    """

    def execute(self):
        run(['git', '--paginate', 'ls-files'])

        self.fm.ui.need_redraw = True
        self.fm.ui.redraw_main_column()


class yarn(Command):
    """:yarn <subcommand>
    """

    def execute(self):
        run(['yarn'] + self.args[1:], shell=True)


    def tab(self, tabnum):

        if len(self.args) > 2 and self.args[1] == 'run':

            from os.path import isfile
            import json

            if not isfile('package.json'):
                self.fm.notify('No package.json in this dir.', bad=True)
                return

            with open('./package.json', mode='r', encoding='utf-8') as f:
                text = f.read()

            x: dict = json.load(open('./package.json', encoding='utf-8'))

            if x.get('scripts', None) == None: return

            return {'yarn run ' + i for i in x['scripts']
                    if self.args[2] in i
                    or len(self.args[-1]) == 1 and i.startswith(self.args[-1])}

        elif len(self.args) == 1 or self.args[1] != 'run':

            return {
                    'yarn ' + i
                    for i in (
                        'install', 'update', 'upgrade', 'remove', 'pack', 'run', 'unlink',
                        'generate-lock-entry', 'import', 'access', 'add', 'autoclean',
                        'create', 'exec', 'publish'
                        ) if self.args[-1] in i or len(self.args) == 1
                    }
        else:
            return




class make(Command):
    """:make <subcommand>

    Run make with specified rule.

    NOTE Must have a Makefile in the same directory.
    """

    def execute(self):
        run(['make'] + self.args[1:], shell=True)


    def tab(self, tabnum):
        from os.path import isfile
        import re

        if not isfile('Makefile'):
            self.fm.notify('No Makefile in this dir.', bad=True)
            return

        with open('./Makefile', mode='r', encoding='utf-8') as f:
            text = f.read()

        pat = re.compile(r'^(\w+):', flags=re.M)

        return {'make ' + i.group(1) for i in pat.finditer(text)}


class mvn(Command):

    """:mvn <subcommand>

    Run make with specified rule.

    NOTE Must have a Makefile in the same directory.
    """

    def execute(self):
        run(['mvn'] + self.args[1:], shell=True)

    def tab(self, tabnum):
        from os.path import isfile

        if not isfile('./pom.xml'):
            return

        return {
                'mvn ' + i
                for i in {
                    'site', 'compile', 'package', 'validate', 'install', 'deploy',
                    'test', 'integration-test', 'clean'
                    } if self.args[-1] in i or len(self.args) == 1
                }


class modified(Command):
    """:modified

    List files modified (Git).

    Same as git --paginate ls-files --modified
    """

    def execute(self):
        run(['git', '--paginate', 'ls-files', '--modified'])

        self.fm.ui.need_redraw = True
        self.fm.ui.redraw_main_column()


class vimdiff(Command):

    """:vimdiff <file1> <file2> | <file1> <file2> <file3>

    Open vim in diff mode with passed files.

    NOTE when you mark them, only the ones in the current directory's will be passed to vim.
         Also, you can diff at most 3 files.
    """

    def execute(self):

        command = ['vim', '-d', '--']

        if len(self.fm.thistab.get_selection()) > 1:
            command.extend([i.path
                            for i in self.fm.thistab.get_selection()][:3])

        elif self.args[1:]:
            command.extend(self.args[1:4])

        else:
            return

        run(command)

        self.fm.ui.need_redraw = True
        self.fm.ui.redraw_main_column()
