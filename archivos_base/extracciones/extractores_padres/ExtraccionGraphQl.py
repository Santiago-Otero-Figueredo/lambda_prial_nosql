
from extracciones.extractores_padres.ExtractorBase import ExtractorBase

from extracciones.extractores_padres.NavegadorPersonalizado import NavegadorPersonalizado

class ExtraccionGraphQl(ExtractorBase):

    def _extraer_contenido_html(self, configurar=False):
        navegador = NavegadorPersonalizado()

        browser = navegador._retornar_browser()
        browser.set_window_size(1920 , 1080)
        browser.maximize_window()
        browser.implicitly_wait(25)

        if configurar == False:
            browser.get(self._url_scrap)

        self._contenido_html = browser
