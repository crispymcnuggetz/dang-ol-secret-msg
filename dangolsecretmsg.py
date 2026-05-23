import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
URL = "https://docs.google.com/document/d/e/2PACX-1vQiVT_Jj04V35C-YRzvoqyEYYzdXHcRyMUZCVQRYCu6gQJX7hbNhJ5eFCMuoX47cAsDW2ZBYppUQITr/pub"

# the unicode symbols 

ENCODERS = (
    '\u2588',  # full block
    '\u2580',  # upper half block
    '\u2591',  # shading
)

# reads and returns a block or int or nothing for unicode

def unicode_data_extractor(span):
    temp = getattr(span, "string", None)
    if temp is None:
        return None

    temp_str = str(temp).strip()

    if temp_str.isdigit():
        return int(temp_str)

    if temp_str in ENCODERS:
        return temp_str

    return None

# this is for the grid size 

def dimension_extractor(data_points):
    x, y = 0, 0

    for item in data_points:
        x = max(x, item[1][0])
        y = max(y, item[1][1])

    return x + 1, y + 1

# do it for the plot, jk. this section places it where it needs to be without it being too spaced out and such

def plot_builder(grid_dims, data, x_scale=1.5, y_scale=3.0, fontsize=12):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, grid_dims[0] * x_scale)
    ax.set_ylim(0, grid_dims[1] * y_scale)
    ax.axis('off')

    for item in data:
        p_unicode = item[0]
        x_cord = item[1][0] * x_scale
        y_cord = item[1][1] * y_scale
        ax.text(x_cord, y_cord, p_unicode, fontsize=12, va="center", ha="center")

    plt.subplots_adjust(bottom=0.745)
    plt.show()


def letter_decoder(url):
    temp_list = []
    num_list = []
    unicode_data = []

    try:
        request = requests.get(url)
    except requests.exceptions.RequestException:
        print("URL Error.")
        return

    request.encoding = request.apparent_encoding
    data = request.text

    soup = BeautifulSoup(data, 'html.parser')
    tokens = soup.find_all("span")

    for item in tokens:
        temp_var = unicode_data_extractor(item)

        if len(temp_list) == 2:
            unicode_data.append(temp_list)
            temp_list = []

        if temp_var is None: 
            continue

        if not isinstance(temp_var, int):
            temp_list.append(temp_var)
            continue

        num_list.append(temp_var)

        if len(num_list) == 2:
            temp_list.append(tuple(num_list))
            num_list = []

    if temp_list:
        unicode_data.append(temp_list)

    if not unicode_data:
        print("Error.")
        return

    plot_builder(
        dimension_extractor(unicode_data),
        unicode_data,
    )


if __name__ == "__main__":
    letter_decoder(URL)

    # i hope you like it, i know its not the best but it was fun to make and i hope you approve of it.
    # i am new to coding, so if you have any suggestions or improvements, please let me know! i hope for more opportunities to learn!