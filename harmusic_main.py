# import pygame as py
from textwrap import fill

import customtkinter as ctk
import requests
from PIL import Image
import io
import webbrowser

# =============== Definição do Logo ===============
app_logo = ctk.CTkImage(light_image=Image.open("assets/logo/transparentlogo.png"), size=(90, 55))


# =============== Definição das Funções ===============
def go_to_link(link):
    webbrowser.open_new_tab(f"{link}")


def get_artist_id():
    artist_name = search_artist.get()
    url = f"https://api.deezer.com/search/artist?q={artist_name}"
    response = requests.get(url)
    data = response.json()

    try:
        frame_main.pack(padx=10, pady=10, fill='both')
        artist = data['data'][0]

        artist_id = artist['id']
        artist_name = artist['name']
        artist_picture = artist['picture']
        artist_number_fans = float(artist['nb_fan'])
        artist_link = artist['link']

        image_converter = requests.get(artist_picture)
        image = Image.open(io.BytesIO(image_converter.content))
        picture_artist = ctk.CTkImage(light_image=image, size=(150, 150))

        label_name_artist.configure(text=artist_name)
        label_picture_artist.configure(image=picture_artist)
        label_picture_artist.image = picture_artist
        label_number_fans.configure(text=f"{artist_number_fans:,} fãs".replace(",", "."), font=("Arial", 15))

        link_button.configure(text="Link do Perfil", command=lambda: go_to_link(artist_link))
        link_button.pack(pady=10)

        # ================ MOSTRAR MUSICAS =============
        show_music(artist_id, artist_name)

    except Exception as e:
        label_name_artist.configure(text=f'Digite o nome de um Artista')
        link_button.pack_forget()
        return e


def show_music(id, artista):
    frame_main_musicas.pack(fill="both", padx=10, pady=10)
    url_musics = f"https://api.deezer.com/search/artist/{id}/top"
    response_musics = requests.get(url_musics)
    data_musics = response_musics.json()
    if not data_musics:
        label_music_list.configure(text=f"Erro ao carregar as musicas", font=("Arial", 25, "bold"))
    else:
        label_music_list.configure(text=f"Top Musicas de {artista}", font=("Arial", 25, "bold"))

    pass


# =============== Definição da Janela ===============
app = ctk.CTk()
app.geometry("750x500")
app.title("Harmusic")
app.iconbitmap("assets/logo/iconharmusic.ico")

# =============== Definição do HEADER ===============
frame_header = ctk.CTkFrame(app)
frame_header.pack(side="top", fill="x")

application_logo = ctk.CTkLabel(frame_header, image=app_logo, text='')
application_logo.pack(side='left')

application_name = ctk.CTkLabel(frame_header, text="Harmusic", font=("Arial", 25))
application_name.pack(pady=10, side='left')

search_artist = ctk.CTkEntry(frame_header, placeholder_text='Ex: Nome cantor')
search_artist.pack(pady=10, padx=10, side='right')

search_button = ctk.CTkButton(frame_header, text="Procurar", command=get_artist_id)
search_button.pack(pady=10, padx=10, side='right')

# =============== Definição da MAIN ===============
frame_main = ctk.CTkFrame(app)

label_name_artist = ctk.CTkLabel(frame_main, text='', font=("Arial", 25))
label_name_artist.pack(pady=10, padx=10)

label_picture_artist = ctk.CTkLabel(frame_main, text='', image=None, font=("Arial", 25))
label_picture_artist.pack()

label_number_fans = ctk.CTkLabel(frame_main, text='')
label_number_fans.pack()

link_button = ctk.CTkButton(frame_main, text='', command=None)
list_artist_music = ctk.CTkButton(frame_main, text='', command=None)

# =============== Definição da MAIN_MUSICAS ===============
frame_main_musicas = ctk.CTkFrame(app)
label_music_list = ctk.CTkLabel(frame_main_musicas, text='')

app.mainloop()
