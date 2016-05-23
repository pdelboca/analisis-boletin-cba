from analisis_boletines_cba.preprocess.regexp_ner import RegExpNERRunner


class ResolucionesNERRunner(RegExpNERRunner):
    def __init__(self, override=False):
        # Expresiones regulares tokenizadas: corren sobre strings tokenizados

        # Ejemplo: Resoluciones Ministeriales N° 00493/2006
        regexp = u'<Resoluciones><Ministeriales>(?P<<number>><Nº><\d+></><\d+>)'
        override = True

        self.increment = True
        super().__init__('resolucion', regexp, override)

    def process_match(self, match):
        # Esto es para extraer, de match de la Expresion Regular, los datos que se guardan
        # Tienen que identificarse grupos en la regexp (?P<<nombre_grupo>>regexp)
        number = ' '.join(match.group('number'))
        kind = self.label
        offset, offset_end = match.span('number')
        entity_oc = self.build_occurrence(number, kind, number, offset, offset_end)

        return entity_oc