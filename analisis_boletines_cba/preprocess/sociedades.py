from analisis_boletines_cba.preprocess.regexp_ner import RegExpNERRunner


class SociedadesNERRunner(RegExpNERRunner):
    def __init__(self, override=False):
        # Expresiones regulares tokenizadas: corren sobre strings tokenizados
        override=True
        # Ejemplo: 'Denominación', 'Social', ':', 'ADMINISTRADORA', 'DE', 'SERVICIOS', 'S', '.', 'A', '.'
        regexp = u'<Denominación><Social><:>(?P<<nombre>><[A-ZÁÉÍÓÚÑ\.]+>+)'

        self.increment = True
        super().__init__('sociedades', regexp, override)

    def process_match(self, match):
        # Esto es para extraer, de match de la Expresion Regular, los datos que se guardan
        # Tienen que identificarse grupos en la regexp (?P<<nombre_grupo>>regexp)
        nombre = ' '.join(match.group('nombre'))
        kind = self.label
        offset, offset_end = match.span('nombre')
        entity_oc = self.build_occurrence(nombre, kind, nombre, offset, offset_end)

        return entity_oc