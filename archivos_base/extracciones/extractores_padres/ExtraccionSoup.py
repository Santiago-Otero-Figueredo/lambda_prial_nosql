from bs4 import BeautifulSoup
from extracciones.extractores_padres.ExtractorBase import ExtractorBase
import requests



class ExtraccionSoup(ExtractorBase):
                    
    
    def _extraer_contenido_html(self) -> "BeautifulSoup":       
        pagina = requests.get(self._url_scrap, verify=False)
        self._contenido_html = BeautifulSoup(pagina.text, 'html.parser')


    def finalizacion_scraping(self) -> None:
        pass

    def implicity_wait_minimo_antes_de_scraping(self, tiempo_maximo) -> None:
        pass