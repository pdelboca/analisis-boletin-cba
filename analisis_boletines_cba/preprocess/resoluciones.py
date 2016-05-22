from analisis_boletines_cba.preprocess.regexp_ner import RegExpNERRunner


class ResolucionesNERRunner(RegExpNERRunner):
    def __init__(self, override=False):
        # Expresiones regulares tokenizadas: corren sobre strings tokenizados

        # Ejemplo: Resoluciones Ministeriales N° 00493/2006
        # regexp = u'<Resoluciones><Ministeriales><Nº><\d+>'

        self.increment = True
        super().__init__('resolucion', regexp, override)