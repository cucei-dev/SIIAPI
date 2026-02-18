import re
from datetime import datetime, time
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup

from app.core.config import settings
from app.core.exceptions import ConflictException, NotFoundException
from app.modules.aula.schemas import AulaCreate
from app.modules.aula.services.aula_service import AulaService
from app.modules.calendario.services.calendario_service import \
    CalendarioService
from app.modules.centro.services.centro_service import \
    CentroUniversitarioService
from app.modules.clase.schemas import ClaseCreate
from app.modules.clase.services.clase_service import ClaseService
from app.modules.edificio.schemas import EdificioCreate
from app.modules.edificio.services.edificio_service import EdificioService
from app.modules.materia.schemas import MateriaCreate
from app.modules.materia.services.materia_service import MateriaService
from app.modules.profesor.schemas import ProfesorCreate
from app.modules.profesor.services.profesor_service import ProfesorService
from app.modules.seccion.schemas import SeccionCreate, SeccionUpdate
from app.modules.seccion.services.seccion_service import SeccionService
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

    def parse_table(self, soup: BeautifulSoup) -> list[dict]:
        tabla = soup.find("table")
        if not tabla:
            return []

        filas = tabla.find_all("tr", recursive=False)
        datos_finales = []
        for tr in filas:
            tds = tr.find_all("td", recursive=False)
            if not tds or not re.match(r"^\d{4,}", tds[0].get_text(strip=True)):
                continue

            def txt(cell):
                return cell.get_text(" ", strip=True)

            base_info = {
                "NRC": txt(tds[0]),
                "Clave": txt(tds[1]) if len(tds) > 1 else None,
                "Materia": txt(tds[2]) if len(tds) > 2 else None,
                "Sec": txt(tds[3]) if len(tds) > 3 else None,
                "CR": txt(tds[4]) if len(tds) > 4 else None,
                "CUP": txt(tds[5]) if len(tds) > 5 else None,
                "DIS": txt(tds[6]) if len(tds) > 6 else None,
            }

            profesor = None
            if len(tds) > 8:
                inner_prof = tds[8].find("table")
                if inner_prof:
                    prof_tr = inner_prof.find("tr")
                    if prof_tr and len(prof_tr.find_all("td")) >= 2:
                        profesor = prof_tr.find_all("td")[1].get_text(" ", strip=True)
                    elif prof_tr:
                        profesor = txt(prof_tr)
                else:
                    profesor = txt(tds[8])

            base_info["Profesor"] = profesor

            horario_str = None
            if len(tds) > 7:
                inner_table = tds[7].find("table")
                if inner_table:
                    parts = []
                    for ir in inner_table.find_all("tr"):
                        parts.append(
                            " | ".join(
                                [c.get_text(" ", strip=True) for c in ir.find_all("td")]
                            )
                        )
                    horario_str = " ; ".join(p for p in parts if p.strip())
                else:
                    horario_str = txt(tds[7])

            if horario_str and horario_str.strip():
                sesiones = horario_str.split(";")
                for sesion in sesiones:
                    partes = [p.strip() for p in sesion.split("|")]
                    fila_expandida = base_info.copy()
                    fila_expandida.update(
                        {
                            "SesionNum": partes[0] if len(partes) > 0 else None,
                            "Horas": partes[1] if len(partes) > 1 else None,
                            "Dias": partes[2] if len(partes) > 2 else None,
                            "Edificio": partes[3] if len(partes) > 3 else None,
                            "Aula": partes[4] if len(partes) > 4 else None,
                            "Periodo": partes[5] if len(partes) > 5 else None,
                        }
                    )
                    datos_finales.append(fila_expandida)
            else:
                fila_vacia = base_info.copy()
                fila_vacia.update(
                    {
                        "SesionNum": None,
                        "Horas": None,
                        "Dias": None,
                        "Edificio": None,
                        "Aula": None,
                        "Periodo": None,
                    }
                )
                datos_finales.append(fila_vacia)

        return datos_finales

    def make_request(
        self, calendario: str, centro: str, limite: int = 15000
    ) -> list[dict]:
        """Make request to SIIAU and return parsed data as list of dicts"""
        payload = {
            "ciclop": calendario,
            "cup": centro,
            "mostrarp": limite,
        }

        response = requests.post(settings.SIIAU_URL, data=payload)
        soup = BeautifulSoup(response.text, "html.parser")

        return self.parse_table(soup)

    def _get_or_create_materia(
        self, clave: str, nombre: str, creditos: int
    ) -> tuple[Any, bool]:
        """Get existing materia or create new one. Returns (materia, created)"""
        materias_db, count = self.materia_service.list_materias(clave=clave)
        if count == 0:
            materia = self.materia_service.create_materia(
                MateriaCreate(name=nombre, creditos=creditos, clave=clave)
            )
            return materia, True
        return materias_db[0], False

    def _get_or_create_profesor(self, nombre: str) -> tuple[Any, bool]:
        """Get existing profesor or create new one. Returns (profesor, created)"""
        profesores_db, count = self.profesor_service.list_profesores(name=nombre)
        if count == 0:
            profesor = self.profesor_service.create_profesor(
                ProfesorCreate(name=nombre)
            )
            return profesor, True
        return profesores_db[0], False

    def _get_or_create_edificio(self, nombre: str, centro_id: int) -> tuple[Any, bool]:
        """Get existing edificio or create new one. Returns (edificio, created)"""
        edificios_db, count = self.edificio_service.list_edificios(
            name=nombre, centro_id=centro_id
        )
        if count == 0:
            edificio = self.edificio_service.create_edificio(
                EdificioCreate(name=nombre, centro_id=centro_id)
            )
            return edificio, True
        return edificios_db[0], False

    def _get_or_create_aula(self, nombre: str, edificio_id: int) -> tuple[Any, bool]:
        """Get existing aula or create new one. Returns (aula, created)"""
        aulas_db, count = self.aula_service.list_aulas(
            name=nombre, edificio_id=edificio_id
        )
        if count == 0:
            aula = self.aula_service.create_aula(
                AulaCreate(name=nombre, edificio_id=edificio_id)
            )
            return aula, True
        return aulas_db[0], False

    def _parse_periodo(
        self, periodo_str: Optional[str]
    ) -> tuple[Optional[datetime], Optional[datetime]]:
        """Parse periodo string into start and end dates"""
        if not periodo_str or periodo_str == "":
            return None, None
        inicio_str, fin_str = periodo_str.split(" - ")
        periodo_inicio = datetime.strptime(inicio_str, "%d/%m/%y")
        periodo_fin = datetime.strptime(fin_str, "%d/%m/%y")
        return periodo_inicio, periodo_fin

    def _parse_horas(
        self, horas_str: Optional[str]
    ) -> tuple[Optional[time], Optional[time]]:
        """Parse horas string into start and end times"""
        if not horas_str or horas_str == "":
            return None, None
        inicio_str, fin_str = horas_str.split("-")
        hora_inicio = time(int(inicio_str[:2]), int(inicio_str[2:]))
        hora_fin = time(int(fin_str[:2]), int(fin_str[2:]))
        return hora_inicio, hora_fin

    def _parse_dias(self, dias_str: Optional[str]) -> list[int]:
        """Parse dias string into list of day numbers"""
        if not dias_str or dias_str == "":
            return [0]
        valores = dias_str.split()
        return [i + 1 for i, dia in enumerate(valores) if dia != "."]

    def _validate_seccion_data(self, data: SeccionSiiau) -> Optional[str]:
        """Validate required fields. Returns error message or None"""
        if not data.NRC or data.NRC == "":
            return "NRC is null"
        if not data.Clave or data.Clave == "":
            return "Clave is null"
        if not data.Materia or data.Materia == "":
            return "Materia is null"
        if not data.Sec or data.Sec == "":
            return "Sec is null"
        return None

    def _create_clases_for_seccion(
        self, data_list: list[SeccionSiiau], seccion_id: int, centro_id: int
    ) -> int:
        """Create clases for a seccion from multiple session records. Returns number of clases created"""
        clases_creadas = 0
        
        for data in data_list:
            # Skip if no schedule data
            if not data.Horas or not data.Dias:
                continue
                
            hora_inicio, hora_fin = self._parse_horas(data.Horas)
            dias = self._parse_dias(data.Dias)
            
            # Get or create edificio and aula for this session
            aula_id = None
            if data.Edificio and data.Edificio != "":
                edificio, _ = self._get_or_create_edificio(data.Edificio, centro_id)
                
                if data.Aula and data.Aula != "":
                    aula, _ = self._get_or_create_aula(data.Aula, edificio.id)
                    aula_id = aula.id

            for dia in dias:
                self.clase_service.create_clase(
                    ClaseCreate(
                        sesion=int(data.SesionNum) if data.SesionNum else None,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin,
                        dia=dia if dia != 0 else None,
                        seccion_id=seccion_id,
                        aula_id=aula_id,
                    )
                )
                clases_creadas += 1
        return clases_creadas

    def _process_seccion(
        self,
        data_list: list[SeccionSiiau],
        calendario_id: int,
        centro_id: int,
        update_if_exists: bool = False,
        full_update: bool = False,
    ) -> dict:
        """Process a seccion with all its session records. Returns stats dict"""
        stats = {
            "materias_creadas": 0,
            "profesores_creados": 0,
            "edificios_creados": 0,
            "aulas_creadas": 0,
            "clases_creadas": 0,
            "secciones_creadas": 0,
            "secciones_actualizadas": 0,
            "error": None,
        }

        # Use first record for base seccion data
        data = data_list[0]

        # Validate data
        error = self._validate_seccion_data(data)
        if error:
            stats["error"] = error
            return stats

        # Check if seccion exists
        secciones_db, count = self.seccion_service.list_secciones(
            nrc=data.NRC, calendario_id=calendario_id
        )
        seccion_exists = count > 0

        if seccion_exists and not update_if_exists:
            stats["error"] = "NRC already in use in that Calendario"
            return stats

        # Get or create materia
        materia, created = self._get_or_create_materia(
            data.Clave, data.Materia, int(data.CR)
        )
        if created:
            stats["materias_creadas"] += 1

        # Get or create profesor
        profesor = None
        if data.Profesor and data.Profesor != "":
            profesor, created = self._get_or_create_profesor(data.Profesor)
            if created:
                stats["profesores_creados"] += 1

        # Parse periodo from first record
        periodo_inicio, periodo_fin = self._parse_periodo(data.Periodo)

        # Create or update seccion
        if seccion_exists:
            seccion = secciones_db[0]
            if seccion.id:
                # Update only the fields that can change
                update_data = SeccionUpdate(
                    name=data.Sec,
                    cupos=int(data.CUP),
                    cupos_disponibles=int(data.DIS),
                    periodo_inicio=periodo_inicio,
                    periodo_fin=periodo_fin,
                    materia_id=materia.id,
                    profesor_id=profesor.id if profesor else None,
                    nrc=None,  # NRC doesn't change
                    centro_id=None,  # Centro doesn't change
                    calendario_id=None,  # Calendario doesn't change
                )
                self.seccion_service.update_seccion(seccion.id, update_data)
                stats["secciones_actualizadas"] += 1

                # Delete existing clases for this seccion
                clases_db, _ = self.clase_service.list_clases(seccion_id=seccion.id)
                for clase in clases_db:
                    if clase.id and full_update:
                        self.clase_service.delete_clase(clase.id)
        else:
            seccion = self.seccion_service.create_seccion(
                SeccionCreate(
                    name=data.Sec,
                    nrc=data.NRC,
                    cupos=int(data.CUP),
                    cupos_disponibles=int(data.DIS),
                    periodo_inicio=periodo_inicio,
                    periodo_fin=periodo_fin,
                    centro_id=centro_id,
                    materia_id=materia.id,
                    profesor_id=profesor.id if profesor else None,
                    calendario_id=calendario_id,
                )
            )
            stats["secciones_creadas"] += 1

        # Create clases for all sessions
        if seccion.id and full_update:
            clases_creadas = self._create_clases_for_seccion(
                data_list, seccion.id, centro_id
            )
            stats["clases_creadas"] = clases_creadas
            
            # Count unique edificios and aulas created
            edificios_vistos = set()
            aulas_vistas = set()
            for session_data in data_list:
                if session_data.Edificio and session_data.Edificio != "":
                    if session_data.Edificio not in edificios_vistos:
                        edificios_vistos.add(session_data.Edificio)
                        edificios_db, count = self.edificio_service.list_edificios(
                            name=session_data.Edificio, centro_id=centro_id
                        )
                        if count == 0:
                            stats["edificios_creados"] += 1
                    
                    if session_data.Aula and session_data.Aula != "":
                        aula_key = f"{session_data.Edificio}:{session_data.Aula}"
                        if aula_key not in aulas_vistas:
                            aulas_vistas.add(aula_key)
                            edificios_db, _ = self.edificio_service.list_edificios(
                                name=session_data.Edificio, centro_id=centro_id
                            )
                            if edificios_db:
                                aulas_db, count = self.aula_service.list_aulas(
                                    name=session_data.Aula, edificio_id=edificios_db[0].id
                                )
                                if count == 0:
                                    stats["aulas_creadas"] += 1

        return stats

    def save_secciones(
        self,
        data: list[dict],
        calendario_id: int,
        centro_id: int,
        update_if_exists: bool = False,
        full_update: bool = False,
    ) -> dict[str, int]:
        """Save or update secciones from SIIAU data"""
        total_stats = {
            "secciones_creadas": 0,
            "secciones_actualizadas": 0,
            "materias_creadas": 0,
            "profesores_creados": 0,
            "edificios_creados": 0,
            "aulas_creadas": 0,
            "clases_creadas": 0,
            "errores": 0,
        }

        # Group records by NRC - multiple records with same NRC represent different sessions
        secciones_agrupadas: dict[str, list[SeccionSiiau]] = {}
        for item in data:
            d = SeccionSiiau(**item)
            nrc = d.NRC
            if nrc not in secciones_agrupadas:
                secciones_agrupadas[nrc] = []
            secciones_agrupadas[nrc].append(d)

        # Process each seccion with all its session records
        for nrc, registros in secciones_agrupadas.items():
            stats = self._process_seccion(registros, calendario_id, centro_id, update_if_exists, full_update)

            if stats["error"]:
                total_stats["errores"] += 1
            else:
                for key in [
                    "secciones_creadas",
                    "secciones_actualizadas",
                    "materias_creadas",
                    "profesores_creados",
                    "edificios_creados",
                    "aulas_creadas",
                    "clases_creadas",
                ]:
                    total_stats[key] += stats[key]

        return total_stats

    def get_secciones(
        self, calendario_id: int, centro_id: int, update_existing: bool = False, full_update: bool = False
    ):
        """
        Fetch and save secciones from SIIAU.

        Args:
            calendario_id: ID of the calendario
            centro_id: ID of the centro universitario
            update_existing: If True, updates existing secciones instead of skipping them

        Returns:
            Dictionary with statistics of the operation
        """
        calendario = self.calendario_service.get_calendario(calendario_id)
        centro = self.centro_service.get_centro(centro_id)

        if not calendario.id or not centro.id:
            raise NotFoundException("Calendario or Centro not found")

        # Single request to SIIAU for all secciones
        secciones = self.make_request(calendario.siiau_id, centro.siiau_id)

        # Process all secciones with update flag
        return self.save_secciones(
            secciones, calendario.id, centro.id, update_if_exists=update_existing, full_update=full_update
        )

    def update_all_secciones(
        self, calendario_id: int, centro_id: int, full_update: bool = False,
    ) -> dict[str, int]:
        """
        Update all existing secciones with fresh data from SIIAU.
        Makes a single request and updates all matching NRCs.

        Args:
            calendario_id: ID of the calendario
            centro_id: ID of the centro universitario

        Returns:
            Dictionary with statistics of the operation
        """
        return self.get_secciones(calendario_id, centro_id, update_existing=True, full_update=full_update)
