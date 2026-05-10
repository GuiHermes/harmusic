# import pygame as py
import customtkinter as ctk
import requests
from PIL import Image
import io
import webbrowser

# =============== Definição da Janela ===============
app = ctk.CTk()
app.geometry("1280x720")
app.title("Harmusic")
app.iconbitmap("assets/logo/iconharmusic.ico")

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
        show_top_music(artist_id)
        show_all_albuns(artist_id)

    except Exception as e:
        label_name_artist.configure(text=f'Digite o nome de um Artista')
        link_button.pack_forget()
        return e


def create_music_tab(music):
    music_link = music['link']
    frame_exib_music = ctk.CTkFrame(scroll_list_top, border_width=3)
    frame_exib_music.pack(padx=10, pady=10, fill='x')
    label_exib_music = ctk.CTkLabel(frame_exib_music, text=music['title_short'], font=("Arial", 25))
    label_exib_music.pack(pady=10, padx=10, fill='x')
    label_rank_music = ctk.CTkLabel(frame_exib_music, text=f"Rank N°{music['rank']}", font=("Arial", 25))
    label_rank_music.pack(pady=5, padx=5, fill='x')
    button_link_music = ctk.CTkButton(frame_exib_music, text='Ir para a musica',
                                      command=lambda link=music_link: go_to_link(link), border_color='white',
                                      border_width=2, corner_radius=55, fg_color='#FFBF00', hover_color='#DEAD21',
                                      text_color='#453506', width=200)
    button_link_music.pack(pady=10)


def show_top_music(identifier):
    tabview.pack(fill="both", expand=True, padx=10, pady=10)
    url_musics = f"https://api.deezer.com/artist/{identifier}/top"
    response_musics = requests.get(url_musics)
    data_musics = response_musics.json()
    musics = data_musics['data']
    for widget in scroll_list_top.winfo_children():
        widget.destroy()
    try:
        for music in musics:
            create_music_tab(music)

    except Exception as e:
        print(e)


def show_all_albuns(artist_id):
    url_albuns = f"https://api.deezer.com/artist/{artist_id}/albums"
    response_albuns = requests.get(url_albuns)
    data_albuns = response_albuns.json()
    albuns = data_albuns['data']
    for widget in scroll_list_albuns.winfo_children():
        widget.destroy()
    try:
        for album in albuns:
            create_album_tab(album)
        pass
    except Exception as e:
        print(e)


def create_album_tab(album):
    album_link = album['link']
    frame_albums = ctk.CTkFrame(scroll_list_albuns, border_width=3)
    frame_albums.pack(pady=10, padx=10, fill='x')
    label_name_albums = ctk.CTkLabel(frame_albums, text=f"{album['title']}", font=("Arial", 25))
    label_name_albums.pack(pady=10, padx=10, side='top')
    label_fans_albums = ctk.CTkLabel(frame_albums, text=f"N° de fãs - {album['fans']}", font=("Sugoi", 15, "bold"))
    label_fans_albums.pack()
    label_release_album = ctk.CTkLabel(frame_albums, text=f"Data de Lançamento:\n{album['release_date']}",
                                       font=("Arial", 25))
    label_release_album.pack(pady=10, padx=10)

    button_link_album = ctk.CTkButton(frame_albums, text='Ir para o album',
                                      command=lambda link=album_link: go_to_link(link), border_color='white',
                                      border_width=2, corner_radius=55, fg_color='#FFBF00', hover_color='#DEAD21',
                                      text_color='#453506', width=200)
    button_link_album.pack(pady=10, padx=10)


def credits_logo():
    pop_up_credit = ctk.CTkToplevel(app)
    pop_up_credit.title("Creditos")
    pop_up_credit.geometry("450x250")
    pop_up_credit.attributes("-topmost", True)
    pop_up_credit.resizable(False, False)
    frame_pop_up = ctk.CTkFrame(pop_up_credit)
    frame_pop_up.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)
    label_pop = ctk.CTkLabel(frame_pop_up, text="Creditos", font=("SUGOI", 25, 'bold'))
    label_pop.pack(side="top", padx=10, pady=10)
    label_up = ctk.CTkLabel(frame_pop_up,
                            text="Harmusic foi feito por \n Guilherme Hermes, super master powered\nlendario, foda, incrivel, absurdamente\n avassalador!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
                            font=("Arial", 15))
    label_up.pack(side="top", padx=10, pady=10)
    button_up = ctk.CTkButton(frame_pop_up, text="Sair", command=lambda: close_pop_up(pop_up_credit),
                              border_color='white',
                              border_width=2, corner_radius=55, fg_color='#FFBF00', hover_color='#DEAD21',
                              text_color='#453506')
    button_up.pack(side="top", padx=10, pady=10)


def close_pop_up(pop):
    pop.destroy()


# =============== Definição do HEADER ===============
frame_header = ctk.CTkFrame(app, border_color='#FFCC70', fg_color='#8D6F3A')
frame_header.pack(side="top", fill="x")

application_logo = ctk.CTkButton(frame_header, image=app_logo, text='', command=credits_logo, fg_color='transparent',
                                 hover_color="#8D6F3A")
application_logo.pack(side='left')

application_name = ctk.CTkLabel(frame_header, text="Harmusic", font=("Arial", 25))
application_name.pack(pady=10, side='left')

search_artist = ctk.CTkEntry(frame_header, placeholder_text='Ex: Nome cantor')
search_artist.pack(pady=10, padx=10, side='right')
search_artist.bind("<Return>", lambda event: get_artist_id())

search_button = ctk.CTkButton(frame_header, text="Procurar", command=get_artist_id, border_color='white',
                              border_width=2, corner_radius=55, fg_color='#FFBF00', hover_color='#DEAD21',
                              text_color='#453506')
search_button.pack(pady=10, padx=10, side='right')

# =============== Definição da MAIN ===============
frame_main = ctk.CTkFrame(app, border_color='#FFCC70', fg_color='#8D6F3A')

label_name_artist = ctk.CTkLabel(frame_main, text='', font=("Arial", 25))
label_name_artist.pack(pady=10, padx=10)

label_picture_artist = ctk.CTkLabel(frame_main, text='', image=None, font=("Arial", 25))
label_picture_artist.pack()

label_number_fans = ctk.CTkLabel(frame_main, text='')
label_number_fans.pack()

link_button = ctk.CTkButton(frame_main, text='', command=None, border_color='white', border_width=2, corner_radius=55,
                            fg_color='#FFBF00', hover_color='#DEAD21', text_color='#453506')
list_artist_music = ctk.CTkButton(frame_main, text='', command=None)

# =============== Definição da MAIN_MUSICAS ===============
tabview = ctk.CTkTabview(app, border_color='#FFCC70', fg_color='#8D6F3A')
tab_top = tabview.add('Top Musicas')
tab_albuns = tabview.add('Todos os Albuns')
#tab_bio = tabview.add('Futura Função a ser implementada')

scroll_list_top = ctk.CTkScrollableFrame(tab_top)
scroll_list_albuns = ctk.CTkScrollableFrame(tab_albuns)
#scroll_list_bio = ctk.CTkScrollableFrame(tab_bio)

scroll_list_top.pack(fill="both", expand=True, padx=10, pady=10)
scroll_list_albuns.pack(fill="both", expand=True, padx=10, pady=10)
#scroll_list_bio.pack(fill="both", expand=True, padx=10, pady=10)

app.mainloop()
