import re
from bs4 import BeautifulSoup
import requests
from app.core.config import settings
from app.modules.centro.services.centro_service import CentroUniversitarioService
from app.modules.calendario.services.calendario_service import CalendarioService
from app.modules.materia.services.materia_service import MateriaService
from app.modules.profesor.services.profesor_service import ProfesorService
from app.modules.edificio.services.edificio_service import EdificioService
from app.modules.seccion.services.seccion_service import SeccionService
from app.modules.aula.services.aula_service import AulaService
from app.modules.clase.services.clase_service import ClaseService
from app.modules.tasks.schemas.siiau import SeccionSiiau

class TasksService:
    def __init__(
        self,
        centro_service: CentroUniversitarioService,
        calendario_service: CalendarioService,
        materia_service: MateriaService,
        profesor_service: ProfesorService,
        edificio_service: EdificioService,
        seccion_service: SeccionService,
        aula_service: AulaService,
        clase_service: ClaseService,
    ):
        self.centro_service = centro_service
        self.calendario_service = calendario_service
        self.materia_service = materia_service
        self.profesor_service = profesor_service
        self.edificio_service = edificio_service
        self.seccion_service = seccion_service
        self.aula_service = aula_service
        self.clase_service = clase_service

    def parse_table(self, soup: BeautifulSoup) -> list[SeccionSiiau]:
        tabla = soup.find('table')
        if not tabla:
            return []

        filas = tabla.find_all('tr', recursive=False)
        datos_finales = []
        for tr in filas:
            tds = tr.find_all('td', recursive=False)
            if not tds or not re.match(r'^\d{4,}', tds[0].get_text(strip=True)):
                continue

            def txt(cell):
                return cell.get_text(' ', strip=True)

            base_info = {
                'NRC': txt(tds[0]),
                'Clave': txt(tds[1]) if len(tds) > 1 else '',
                'Materia': txt(tds[2]) if len(tds) > 2 else '',
                'Sec': txt(tds[3]) if len(tds) > 3 else '',
                'CR': txt(tds[4]) if len(tds) > 4 else '',
                'CUP': txt(tds[5]) if len(tds) > 5 else '',
                'DIS': txt(tds[6]) if len(tds) > 6 else '',
            }

            profesor = ''
            if len(tds) > 8:
                inner_prof = tds[8].find('table')
                if inner_prof:
                    prof_tr = inner_prof.find('tr')
                    if prof_tr and len(prof_tr.find_all('td')) >= 2:
                        profesor = prof_tr.find_all('td')[1].get_text(' ', strip=True)
                    elif prof_tr:
                        profesor = txt(prof_tr)
                else:
                    profesor = txt(tds[8])
            base_info['Profesor'] = profesor

            horario_str = ''
            if len(tds) > 7:
                inner_table = tds[7].find('table')
                if inner_table:
                    parts = []
                    for ir in inner_table.find_all('tr'):
                        parts.append(' | '.join([c.get_text(' ', strip=True) for c in ir.find_all('td')]))
                    horario_str = ' ; '.join(p for p in parts if p.strip())
                else:
                    horario_str = txt(tds[7])

            if horario_str.strip():
                sesiones = horario_str.split(';')
                for sesion in sesiones:
                    partes = [p.strip() for p in sesion.split('|')]
                    fila_expandida = base_info.copy()
                    fila_expandida.update({
                        'SesionNum': partes[0] if len(partes) > 0 else '',
                        'Horas': partes[1] if len(partes) > 1 else '',
                        'Dias': partes[2] if len(partes) > 2 else '',
                        'Edificio': partes[3] if len(partes) > 3 else '',
                        'Aula': partes[4] if len(partes) > 4 else '',
                        'Periodo': partes[5] if len(partes) > 5 else '',
                    })
                    datos_finales.append(fila_expandida)
            else:
                fila_vacia = base_info.copy()
                fila_vacia.update({
                    'SesionNum': '', 'Horas': '', 'Dias': '', 'Edificio': '', 'Aula': '', 'Periodo': ''
                })
                datos_finales.append(fila_vacia)

        return datos_finales

    def make_request(self, calendario: str, centro: str, limite: int = 15000) -> list[SeccionSiiau]:
        payload = {
            "ciclop": calendario,
            "cup": centro,
            "mostrarp": limite,
        }

        response = requests.post(settings.SIIAU_URL, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')

        return self.parse_table(soup)

    def get_secciones(self, calendario_id: int, centro_id: int) -> int:
        calendario = self.calendario_service.get_calendario(calendario_id)
        centro = self.centro_service.get_centro(centro_id)

        secciones = self.make_request(calendario.siiau_id, centro.siiau_id)
        return len(secciones)
