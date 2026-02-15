import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime, time
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
from app.core.exceptions import ConflictException
from app.modules.materia.schemas import MateriaCreate
from app.modules.profesor.schemas import ProfesorCreate
from app.modules.seccion.schemas import SeccionCreate
from app.modules.edificio.schemas import EdificioCreate
from app.modules.aula.schemas import AulaCreate
from app.modules.clase.schemas import ClaseCreate

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
                'Clave': txt(tds[1]) if len(tds) > 1 else None,
                'Materia': txt(tds[2]) if len(tds) > 2 else None,
                'Sec': txt(tds[3]) if len(tds) > 3 else None,
                'CR': txt(tds[4]) if len(tds) > 4 else None,
                'CUP': txt(tds[5]) if len(tds) > 5 else None,
                'DIS': txt(tds[6]) if len(tds) > 6 else None,
            }

            profesor = None
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

            horario_str = None
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
                        'SesionNum': partes[0] if len(partes) > 0 else None,
                        'Horas': partes[1] if len(partes) > 1 else None,
                        'Dias': partes[2] if len(partes) > 2 else None,
                        'Edificio': partes[3] if len(partes) > 3 else None,
                        'Aula': partes[4] if len(partes) > 4 else None,
                        'Periodo': partes[5] if len(partes) > 5 else None,
                    })
                    datos_finales.append(fila_expandida)
            else:
                fila_vacia = base_info.copy()
                fila_vacia.update({
                    'SesionNum': None, 'Horas': None, 'Dias': None, 'Edificio': None, 'Aula': None, 'Periodo': None
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

    def save_secciones(self, data: list[SeccionSiiau], calendario_id: int, centro_id: int) -> dict[str, int]:
        errors = []
        secciones_creadas = 0
        materias_creadas = 0
        profesores_creados = 0
        edificios_creados = 0
        aulas_creadas = 0
        clases_creadas = 0

        for i in data:
            d = SeccionSiiau(**i)
            if not d.NRC or d.NRC == "":
                errors.append(ConflictException("NRC is null"))
                continue

            _,secciones = self.seccion_service.list_secciones(nrc=d.NRC, calendario_id=calendario_id)

            if secciones != 0:
                errors.append(ConflictException("NRC already in use in that Calendario"))
                continue
            
            if not d.Clave or d.Clave == "":
                errors.append(ConflictException("Clave is null"))
                continue

            if not d.Materia or d.Materia == "":
                errors.append(ConflictException("Materia is null"))
                continue

            materias_db,materias = self.materia_service.list_materias(clave=d.Clave)

            if materias == 0:
                materias_creadas += 1
                materia = self.materia_service.create_materia(
                    MateriaCreate(
                        name=d.Materia,
                        creditos=int(d.CR),
                        clave=d.Clave,
                    )
                )
            else:
                materia = materias_db[0]

            if not d.Profesor or d.Profesor == "":
                profesor = None
            else:
                profesores_db,profesores = self.profesor_service.list_profesores(name=d.Profesor)

                if profesores == 0:
                    profesores_creados += 1
                    profesor = self.profesor_service.create_profesor(
                        ProfesorCreate(
                            name=d.Profesor,
                        )
                    )
                else:
                    profesor = profesores_db[0]
            
            if not d.Sec or d.Sec == "":
                errors.append(ConflictException("Sec is null"))
                continue

            if not d.Periodo or d.Periodo == "":
                periodo_inicio = None
                periodo_fin = None
            else:
                inicio_str, fin_str = d.Periodo.split(" - ")
                periodo_inicio = datetime.strptime(inicio_str, "%d/%m/%y")
                periodo_fin = datetime.strptime(fin_str, "%d/%m/%y")

            secciones_creadas += 1
            seccion = self.seccion_service.create_seccion(
                SeccionCreate(
                    name=d.Sec,
                    nrc=d.NRC,
                    cupos=int(d.CUP),
                    cupos_disponibles=int(d.DIS),
                    periodo_inicio=periodo_inicio,
                    periodo_fin=periodo_fin,
                    centro_id=centro_id,
                    materia_id=materia.id,
                    profesor_id=profesor.id if profesor else None,
                    calendario_id=calendario_id
                )
            )

            if not d.Edificio or d.Edificio == "":
                edificio = None
            else:
                edificios_db,edificios = self.edificio_service.list_edificios(name=d.Edificio, centro_id=centro_id)

                if edificios == 0:
                    edificios_creados += 1
                    edificio = self.edificio_service.create_edificio(
                        EdificioCreate(
                            name=d.Edificio,
                            centro_id=centro_id,
                        )
                    )
                else:
                    edificio = edificios_db[0]
            
            if not d.Aula or d.Aula == "":
                aula = None
            elif edificio:
                aulas_db,aulas = self.aula_service.list_aulas(name=d.Aula, edificio_id=edificio.id)

                if aulas == 0:
                    aulas_creadas += 1
                    aula = self.aula_service.create_aula(
                        AulaCreate(
                            name=d.Aula,
                            edificio_id=edificio.id
                        )
                    )
                else:
                    aula = aulas_db[0]
            else:
                aula = None
            
            if not d.Horas or d.Horas == "":
                hora_inicio = None
                hora_fin = None
            else:
                inicio_str, fin_str = d.Horas.split("-")
                hora_inicio = time(int(inicio_str[:2]), int(inicio_str[2:]))
                hora_fin = time(int(fin_str[:2]), int(fin_str[2:]))

            if not d.Dias or d.Dias == "":
                dias = [0]
            else:
                valores = d.Dias.split()
                dias = [i + 1 for i, dia in enumerate(valores) if dia != "."]

            for dia in dias:
                # try:
                clases_creadas += 1
                self.clase_service.create_clase(
                    ClaseCreate(
                        sesion=int(d.SesionNum) if d.SesionNum else None,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin,
                        dia=dia if dia != 0 else None,
                        seccion_id=seccion.id,
                        aula_id=aula.id if aula else None,
                    )
                )
                # except Exception as e:
                #     errors.append(e)
        
        return {
            "secciones_creadas": secciones_creadas,
            "materias_creadas": materias_creadas,
            "profesores_creados": profesores_creados,
            "edificios_creados": edificios_creados,
            "aulas_creadas": aulas_creadas,
            "clases_creadas": clases_creadas,
            "errores": len(errors),
        }

    def get_secciones(self, calendario_id: int, centro_id: int):
        calendario = self.calendario_service.get_calendario(calendario_id)
        centro = self.centro_service.get_centro(centro_id)

        secciones = self.make_request(calendario.siiau_id, centro.siiau_id)
        return self.save_secciones(secciones, calendario.id, centro.id)
