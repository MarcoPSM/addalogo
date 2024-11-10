import os
from tkinter import Tk, Label, Button, filedialog, messagebox, StringVar, Text, Scrollbar, END, font, Frame
from PIL import Image, ExifTags
from heic2png import HEIC2PNG

class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("Add a Logo")

        self.label = Label(master, text="Selecione as pastas de entrada e saída")
        self.label.pack()

        self.in_folder_var = StringVar()
        self.out_folder_var = StringVar()

        self.in_folder_var.set(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'in'))
        self.out_folder_var.set(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'out'))

        self.select_in_button = Button(master, text="Selecionar Pasta de Entrada", command=self.select_in_folder)
        self.select_in_button.pack()
        
        self.in_folder_label = Label(master, textvariable=self.in_folder_var)
        self.in_folder_label.pack()

        self.select_out_button = Button(master, text="Selecionar Pasta de Saída", command=self.select_out_folder)
        self.select_out_button.pack()

        self.out_folder_label = Label(master, textvariable=self.out_folder_var)
        self.out_folder_label.pack()

        bold_font = font.Font(weight="bold")
        self.process_button = Button(master, text="Processar Imagens", command=self.process_images, font=bold_font)
        self.process_button.pack()

        # Frame para agrupar a área de texto e a barra de rolagem
        self.text_frame = Frame(master)
        self.text_frame.pack(padx=10, pady=5, fill='both', expand=True)

        self.text_area = Text(self.text_frame, height=10, width=50)
        self.text_area.pack(side='left', fill='both', expand=True)

        self.scrollbar = Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area['yscrollcommand'] = self.scrollbar.set

        self.logo_file_name = 'logo.png'
        self.recognized_extensions = ['.jpg', '.jpeg', '.png', '.heic']

    def select_in_folder(self):
        self.in_folder_var.set(filedialog.askdirectory())
        messagebox.showinfo("Pasta de Entrada", f"Pasta de entrada selecionada: {self.in_folder_var.get()}")

    def select_out_folder(self):
        self.out_folder_var.set(filedialog.askdirectory())
        messagebox.showinfo("Pasta de Saída", f"Pasta de saída selecionada: {self.out_folder_var.get()}")

    def process_images(self):
        in_folder = self.in_folder_var.get()
        out_folder = self.out_folder_var.get()

        if not in_folder or not out_folder:
            messagebox.showerror("Erro", "Por favor, selecione as pastas de entrada e saída.")
            return

        for old in os.listdir(out_folder):
            os.remove(os.path.join(out_folder, old))

        watermark = Image.open(self.logo_file_name)
        for image in os.listdir(in_folder):
            extension = os.path.splitext(image)[1].lower()
            name = os.path.splitext(image)[0]
            self.text_area.insert(END, f"{name} {extension}\n")
            self.text_area.see(END)
            if extension not in self.recognized_extensions:
                self.text_area.insert(END, f"{image} Unrecognized extension\n")
                self.text_area.see(END)
                continue

            if extension == '.heic':
                heic_img = HEIC2PNG(os.path.join(in_folder, image), quality=90)
                heic_img.save()
                os.remove(os.path.join(in_folder, image))
                image = name + '.png'

            photo = Image.open(os.path.join(in_folder, image))
            try:
                if photo._getexif():
                    exif = dict((ExifTags.TAGS[k], v) for k, v in photo._getexif().items() if k in ExifTags.TAGS)
                    if exif.get('Orientation') == 3:
                        photo = photo.rotate(180, expand=True)
                    elif exif.get('Orientation') == 6:
                        photo = photo.rotate(270, expand=True)
                    elif exif.get('Orientation') == 8:
                        photo = photo.rotate(90, expand=True)
            except:
                pass

            x, y = photo.size
            tmp_wm = watermark.resize((int(x / 5), int(y / 5)))
            photo.paste(tmp_wm, (int(x / 2) - int(tmp_wm.size[0] / 2), int(y / 2) - tmp_wm.size[1]), tmp_wm)
            photo = photo.convert('RGB')
            photo.save(os.path.join(out_folder, image.split('.')[0] + '.jpeg'), 'jpeg')
            self.text_area.insert(END, f"{image} --- OK\n")
            self.text_area.see(END)

        messagebox.showinfo("Concluído", "Processamento de imagens concluído!")

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
