# Built-in
import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import messagebox

# 3rd Party
from pygments import lex
from pygments.lexers.data import YamlLexer as Lexer
from pygments.token import Generic
from pygments.styles import get_style_by_name

# from PIL import Image, ImageTk
# main_photo = ImageTk.PhotoImage(Image.open("my_img.png"))
# my_label = Label(image=my_image)

# Own
from runup.version import RUNUP_VERSION


class Editor:

    def __init__(self):

        # ----------------------- #
        # Create helper variables #
        # ----------------------- #
        self._filename = ''
        self._tabsize = 2
        self._file_has_changed = False
        self._selection = None

        # ------------------ #
        # Create main window #
        # ------------------ #
        self.root = tk.Tk()
        self.root.title(f"RunUp Editor v{RUNUP_VERSION} - Free Version")
        # root.iconbitmap('./assets/ico/favicon.ico')
        self.root.geometry("850x700")
        self.root.config(bg="black")
        self.root.wait_visibility(self.root)
        self.root.wm_attributes('-alpha', 0.95)
        self.root.grid_columnconfigure(1, weight=1)

        self.frame_editor = tk.Frame(self.root, width=100, height=400)
        self.frame_editor.pack(fill='both', expand=1)

        # ---------------- #
        # Define Scrollbar #
        # ---------------- #
        scroll_y = tk.Scrollbar(self.frame_editor)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = tk.Scrollbar(self.frame_editor, orient='horizontal')
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # ----------------------- #
        # Define Editor variables #
        # ----------------------- #
        self._editor = tk.Text(
            self.frame_editor, 
            bg="Black", 
            insertbackground="white", 
            fg="white",
            font="TkFixedFont",
            padx=10,
            pady=10,
            undo=True,
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            wrap="none"
        )
        # Link scrollbars to editor
        scroll_y.config(command=self._editor.yview)
        scroll_x.config(command=self._editor.xview)
        # Set Tab size
        tmp_font = tkfont.Font(font=self._editor['font'])
        self._editor.config(tabs=tmp_font.measure(' '*self._tabsize))
        self._editor.pack(fill=tk.BOTH, expand=tk.YES)

        self._lexer = Lexer()
        self._syntax_highlighting_tags = self._editor_load_style("monokai")
        
        # bind each key release to the yaml checker function
        self._editor.bind("<KeyRelease>", lambda _: self.event_editor_key_release())

        # ----------- #
        # Define Menu #
        # ----------- #
        self.main_menu = tk.Menu(self.root)
        self.root.config(menu=self.main_menu)

        # File menu
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.file_new)
        self.file_menu.add_command(label="Open", command=self.file_open)
        self.file_menu.add_command(label="Save", command=self.file_save)
        self.file_menu.add_command(label="Save as", command=self.file_save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open Template", command=self.file_open_template)
        self.file_menu.add_command(label="Save as Template")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Activation Key")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Help edit
        self.help_edit = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Edit", menu=self.help_edit)
        self.help_edit.add_command(label="Select All", command=self._select_all, accelerator=self._accelerator_select_all())
        self.help_edit.add_separator()
        self.help_edit.add_command(label="Copy", accelerator=self._accelerator_copy())
        self.help_edit.add_command(label="Cut", accelerator=self._accelerator_cut())
        self.help_edit.add_command(label="Paste", accelerator=self._accelerator_paste())
        self.help_edit.add_separator()
        self.help_edit.add_command(label="Undo", command=self._editor.edit_undo, accelerator=self._accelerator_undo())
        self.help_edit.add_command(label="Redo", command=self._editor.edit_redo, accelerator=self._accelerator_redo())
        self.help_edit.add_separator()
        self.help_edit.add_command(label="Insert directory")

        # Backup menu
        self.backup_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Backup", menu=self.backup_menu)
        self.backup_menu.add_command(label="Create Backup", state=tk.DISABLED)
        self.backup_menu.add_command(label="Restore Backup", state=tk.DISABLED)
        self.backup_menu.add_separator()
        self.backup_menu.add_command(label="Autimatic Backup", state=tk.DISABLED)
        self.backup_menu.add_separator()
        self.backup_menu.add_command(label="View Jobs", state=tk.DISABLED)
        self.backup_menu.add_command(label="Remove Jobs", state=tk.DISABLED)

        # Help menu
        self.help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Getting Started")
        self.help_menu.add_command(label="Documentation")
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Check for Updates")
        self.help_menu.add_separator()
        self.help_menu.add_command(label="View License")
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About")

        # ----------------- #
        # Define Status bar #
        # ----------------- #
        status = tk.Label(self.root, text=self.status('Ready'), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status.pack(fill='x')

        # -------------------- #
        # Initialize main loop #
        # -------------------- #
        self.root.mainloop()

    def file_save(self):
        if self._filename != '':
            with open(self._filename, 'w') as f:
                f.write(self._editor.get('1.0', tk.END))
        else:
            self.file_save_as()

    def file_save_as(self):
        textfile = filedialog.asksaveasfilename(
            defaultextension=".yaml",
            initialdir=".",
            initialfile="runup.yaml",
            filetypes=(("RunUp YAML files", "runup.yaml runup.yml"),)
        )

        if textfile:
            if textfile.rsplit(os.sep, 1)[1] in ['runup.yaml', 'runup.yml']:
                # name = textfile.rsplit(os.sep, 2)[1]
                with open(textfile, 'w') as f:
                    f.write(self._editor.get('1.0', tk.END))
            else:
                messagebox.showwarning('Warning', 'Invalid filename. File not saved.')
        
    def file_new(self):
        if self._file_has_changed:
            user_said = messagebox.askquestion(
                title="Confirmation",
                message="All the unsaved changes are going to be lost.\n" \
                    + "Are you sure you want to continue?"
            )

        if not self._file_has_changed or user_said == 'yes':
            self._editor.delete('1.0', tk.END)
            self._file_has_changed = False
            self._filename = ''
            # Enable/Disable Menu items
            self.backup_menu.entryconfigure("Create Backup", state=tk.DISABLED)
            self.backup_menu.entryconfigure("Restore Backup", state=tk.DISABLED)
            self.backup_menu.entryconfigure("Autimatic Backup", state=tk.DISABLED)
            self.backup_menu.entryconfigure("View Jobs", state=tk.DISABLED)
            self.backup_menu.entryconfigure("Remove Jobs", state=tk.DISABLED)

    def file_open(self):

        if self._file_has_changed:
            user_said = messagebox.askquestion(
                title="Confirmation",
                message="All the unsaved changes are going to be lost.\n" \
                    + "Are you sure you want to continue?"
            )

        if not self._file_has_changed or user_said == 'yes':
            selected_file = filedialog.askopenfilename(
                initialdir='.',
                title='Select a RunUp YAML file',
                filetypes=(
                    ("Runup YAML", "runup.yaml runup.yml"),
                )
            )
            if selected_file != '':
                # Store selected file
                self._filename = selected_file
                # Delete previous content
                self._editor.delete('1.0', tk.END)
                # Open new file
                with open(self._filename) as f:
                    self._editor.insert(tk.END, f.read())
                # Highlight YAML syntax
                self._editor_check_yaml(start='1.0', end=tk.END)
                # Reset _file_has_changed variable
                self._file_has_changed = False
                # Enable/Disable Menu items
                self.backup_menu.entryconfigure('Create Backup', state=tk.NORMAL)
                self.backup_menu.entryconfigure("Restore Backup", state=tk.NORMAL)
                self.backup_menu.entryconfigure("Autimatic Backup", state=tk.NORMAL)
                self.backup_menu.entryconfigure("View Jobs", state=tk.NORMAL)
                self.backup_menu.entryconfigure("Remove Jobs", state=tk.NORMAL)

    def file_open_template(self):
        # self._editor.delete('1.0', tk.END)
        # with open(self._filename) as f:
        #     self._editor.insert(tk.END, f.read())
        # self._file_has_changed = False
        # Enable/Disable Menu items
        self.backup_menu.entryconfigure("Create Backup", state=tk.DISABLED)
        self.backup_menu.entryconfigure("Restore Backup", state=tk.DISABLED)
        self.backup_menu.entryconfigure("Autimatic Backup", state=tk.DISABLED)
        self.backup_menu.entryconfigure("View Jobs", state=tk.DISABLED)
        self.backup_menu.entryconfigure("Remove Jobs", state=tk.DISABLED)

    def status(self, status):
        val = 'Version: ' \
            + RUNUP_VERSION \
            + (' '*15) \
            + 'Tab Size: ' \
            + str(self._tabsize) \
            + (' '*15) \
            + "Status: " \
            + status
        return val

    def event_editor_key_release(self):
        # Highlight YAML sintax
        self._editor_check_yaml()
        # Indicate the file has changed
        self._file_has_changed = True

    def _accelerator_copy(self):
        if sys.platform.startswith('linux'):
            return '(Ctrl+c)'
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            return '(Ctrl+c)'
        elif sys.platform.startswith('darwin'):
            return '(Cmd+c)'
        else:
            return ''

    def _accelerator_cut(self):
        if sys.platform.startswith('linux'):
            return '(Ctrl+x)'
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            return '(Ctrl+x)'
        elif sys.platform.startswith('darwin'):
            return '(Cmd-x)'
        else:
            return ''

    def _accelerator_paste(self):
        if sys.platform.startswith('linux'):
            return '(Ctrl+v)'
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            return '(Ctrl+v)'
        elif sys.platform.startswith('darwin'):
            return '(Cmd-v)'
        else:
            return ''

    def _accelerator_redo(self):
        if sys.platform.startswith('linux'):
            return '(Ctrl+Shift+z)'
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            return '(Ctrl+y)'
        elif sys.platform.startswith('darwin'):
            return '(Cmd+Shift+z)'
        else:
            return ''

    def _accelerator_select_all(self):
        if sys.platform.startswith('linux'):
            return '(Ctrl+a)'
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            return '(Ctrl+a)'
        elif sys.platform.startswith('darwin'):
            return '(Cmd+a)'
        else:
            return ''

    def _accelerator_undo(self):
        if sys.platform.startswith('linux'):
            return '(Ctrl+z)'
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            return '(Ctrl+z)'
        elif sys.platform.startswith('darwin'):
            return '(Cmd-z)'
        else:
            return ''

    def _editor_check_yaml(self, start='insert linestart', end='insert lineend'):
        data = self._editor.get(start, end)
        while data and data[0] == '\n':
            start = self._editor.index('%s+1c' % start)
            data = data[1:]
        self._editor.mark_set('range_start', start)
        # clear tags
        for t in self._syntax_highlighting_tags:
            self._editor.tag_remove(t, start, "range_start +%ic" % len(data))
        # parse text
        for token, content in lex(data, self._lexer):
            self._editor.mark_set("range_end", "range_start + %ic" % len(content))
            for t in token.split():
                self._editor.tag_add(str(t), "range_start", "range_end")
            self._editor.mark_set("range_start", "range_end")

    def _editor_load_style(self, stylename):
        style = get_style_by_name(stylename)
        syntax_highlighting_tags = []
        for token, opts in style.list_styles():
            kwargs = {}
            fg = opts['color']
            if fg:
                kwargs['foreground'] = '#' + fg
            self._editor.tag_configure(str(token), **kwargs)
            syntax_highlighting_tags.append(str(token))

        self._editor.tag_configure(str(Generic.StrongEmph), font=('Monospace', 10, 'bold', 'italic'))
        syntax_highlighting_tags.append(str(Generic.StrongEmph))
        return syntax_highlighting_tags

    def _select_all(self):
        self._editor.tag_add('sel', '1.0', 'end')

if __name__ == '__main__':

    Editor()
