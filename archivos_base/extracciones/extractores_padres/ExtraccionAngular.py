
from extracciones.extractores_padres.ExtractorBase import ExtractorBase

from extracciones.extractores_padres.NavegadorPersonalizado import NavegadorPersonalizado

class ExtraccionAngular(ExtractorBase):


    def _extraer_contenido_html(self, configurar=False):
        navegador = NavegadorPersonalizado()

        browser = navegador._retornar_browser()
        
        browser.get(self._url_scrap)
        browser.set_window_size(1920 , 1080)
        browser.maximize_window()
        browser.implicitly_wait(10)

        self._contenido_html = browser