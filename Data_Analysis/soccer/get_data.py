from os import makedirs, path, remove
import requests
import zipfile

"""
Este script se encarga de descargar los datos de la página web football-data.co.uk
Sólo para las ligas de los países que se encuentran en la lista list_countries
Estos son los primarios, pero hay más países en la página web
"""

list_season = ["2022/2023", "2021/2022", "2020/2021", "2019/2020", "2018/2019", "2017/2018", "2016/2017", "2015/2016",
               "2014/2015", "2013/2014", "2012/2013", "2011/2012", "2010/2011", "2009/2010", "2008/2009", "2007/2008",
               "2006/2007", "2005/2006"]


list_countries = ["England", "Scotland", "Germany", "Spain", "Italy", "France", "Netherlands", "Belgium", "Portugal",
                  "Turkey", "Greece"]

divisions = {"England": {"E0": "Premier League", "E1": "Championship", "E2": "League 1", "E3": "League 2", "EC": "Conference"},
             "Scotland": {"SC0": "Premiership", "SC1": "Championship", "SC2": "League 1", "SC3": "League 2"},
             "Germany": {"D1": "Bundesliga 1", "D2": "Bundesliga 2"},
             "Spain": {"SP1": "La Liga", "SP2": "La Liga 2"},
             "Italy": {"I1": "Serie A", "I2": "Serie B"},
             "France": {"F1": "Ligue 1", "F2": "Ligue 2"},
             "Netherlands": {"N1": "Eredivisie"},
             "Belgium": {"B1": "Jupiler League"},
             "Portugal": {"P1": "Liga I"},
             "Turkey": {"T1": "Super Lig"},
             "Greece": {"G1": "Ethniki Katigoria"}
             }


def season_to_string(season):
    """Convierte la temporada a un string para poder usarlo en la url"""
    return season[2:4] + season[-2:], season.replace("/", "-")


def get_data_country_by_season(country, season):
    """
    :param country: País del que se quiere obtener los datos
    :param season: Temporada de la que se quiere obtener los datos
    :return: Mensaje indicandome si se pudo o no descargar el país
    """

    print(f"    Descargando datos de {country} temporada {season}...")
    season_code, season_format = season_to_string(season)

    # Para cada división del país, obtengo los datos
    # Ejemplo: https://www.football-data.co.uk/mmz4281/2021/E0.csv
    for division in divisions[country]:
        url = f"https://www.football-data.co.uk/mmz4281/{season_code}/{division}.csv"

        try:
            response = requests.get(url)
            # Si no existe el archivo, lo crea.
            # El archivo se crea en un directorio llamado data
            if not path.exists(f"data/soccer/countries/{country}/{season_format}"):
                makedirs(f"data/soccer/countries/{country}/{season_format}")

            if response.status_code == 200:
                with open(f"data/soccer/countries/{country}/{season_format}/{divisions[country][division]}.csv", "wb") as file:
                    file.write(response.content)
            else:
                print(
                    f"Error al descargar la división {division} de la temporada {season_format} del país {country}")

        except:
            return f"Error al descargar la división {division} de la temporada {season_format} del país {country}"


def get_data_country_seasons_csv(country):
    """
    :param country: País del que se quiere obtener los datos
    :return: Mensaje indicandome si se pudo o no descargar el país
    """

    print(f"Descargando datos de {country}...")

    for season in list_season:
        get_data_country_by_season(country, season)


def get_data_countries_all():
    """Obtiene los datos de todos los países"""
    for country in list_countries:
        get_data_country_seasons_csv(country)


def get_notes():
    """Obtiene las notas del formato xlsx de la página web de football-data.co.uk"""
    url = "https://www.football-data.co.uk/notes.txt"
    response = requests.get(url)
    # Si no existe el archivo, lo crea.
    # El archivo se crea en un directorio llamado data
    if not path.exists("data/soccer"):
        makedirs("data/soccer")
    with open("data/soccer/notes.txt", "w") as file:
        file.write(response.text)


def get_data_season_csv(season):
    """
    :param season: Temporada de la que se quiere obtener los datos
    :return: Mensaje indicandome si se pudo o no descargar la temporada
    """

    print(f"Descargando datos de la temporada {season}...")

    season_code, season_format = season_to_string(season)
    url = f"https://www.football-data.co.uk/mmz4281/{season_code}/data.zip"

    try:
        response = requests.get(url)
        # Si no existe el archivo, lo crea.

    except:
        return f"Error al descargar la temporada {season_format}"

    if not path.exists("data/soccer/seasons"):
        makedirs("data/soccer/seasons")

    with open(f"data/soccer/seasons/{season_format}.zip", "wb") as file:
        file.write(response.content)

    # Descomprimir el archivo
    with zipfile.ZipFile(f"data/soccer/seasons/{season_format}.zip", "r") as zip_ref:
        zip_ref.extractall(f"data/soccer/seasons/{season_format}")

        print(f"Temporada {season_format} descargada correctamente")

    # Eliminar el archivo zip
    remove(f"data/soccer/seasons/{season_format}.zip")

    return f"OK"


def get_data_season_all():
    """Obtiene los datos de todas las temporadas"""
    for season in list_season:
        get_data_season_csv(season)


def get_data_all():
    """Obtiene los datos de todos los países y todas las temporadas"""
    get_data_countries_all()
    get_data_season_all()


def main():
    # Ejecutar pruebas según lo que se quiera hacer
    print("1: notas, 2: datos de una temporada, 3: datos de todas las temporadas, 4: datos de todos los países y todas las temporadas, 5. Datos de un país y todas las temporadas")
    option = input("¿Qué quieres hacer? ")
    if option == "1":
        get_notes()
    elif option == "2":
        season = input("Introduce la temporada: ")
        get_data_season_csv(season)
    elif option == "3":
        get_data_season_all()
    elif option == "4":
        get_data_all()
    elif option == "5":
        print("Países: England, Scotland, Germany, Spain, Italy, France, Netherlands, Belgium, Portugal, Turkey, Greece")
        country = input("Introduce el país: ")
        get_data_country_seasons_csv(country)


if __name__ == "__main__":
    main()
