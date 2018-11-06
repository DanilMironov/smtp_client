import tkinter as tk


class FormRedactor:

    @staticmethod
    def extract_info(thing: tk.Text, is_list=False):
        if is_list:
            return thing.get(1.0, 50.0)[0:-1].split('\n')
        else:
            return thing.get(1.0, 50.0)[0:-1]

    @staticmethod
    def make_button(root, text: str, command):
        frame_btn = tk.Frame(root,
                             bd=10)
        btn = tk.Button(frame_btn,
                        text=text,
                        width=50,
                        height=2,
                        bg='lightgrey',
                        command=command
                        )
        frame_btn.pack(side='top')
        btn.pack(side='top')
        return btn

    @staticmethod
    def make_field(root, text_label, label_height=1, text_height=1, width=50, font='TimesNewRoman 12'):
        label = tk.Label(root,
                         text=text_label,
                         height=label_height,
                         width=width,
                         font=font,
                         )
        text = tk.Text(root,
                       height=text_height,
                       width=width,
                       font=font,
                       )
        label.pack(side='top')
        text.pack(side='top')
        return text

    @staticmethod
    def make_message_field(root, text_label='Message'):
        return FormRedactor.make_field(root, text_label, text_height=9)

    @staticmethod
    def make_window(root, size_x=600, size_y=300):
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        root.geometry('{0}x{1}+{2}+{3}'.format(size_x, size_y, int(screen_w / 4), int(screen_h / 4)))
        return root

