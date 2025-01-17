from inspect import getframeinfo, currentframe
from multiprocessing import current_process


from ede.ede._logger import logger

def fn5E2(conn, return_dict):
    """ 
    6.2 Contenido mínimo, letra b.2
    Validar que los reemplazos no idóneos sean registrados por el director o quien él designe y que exista la observación indicando la falta del docente, 
    junto al nombre y verificador de identidad de quien reemplaza.
    
    Args:
        conn ([sqlalchemy.engine.Connection]): [
          Objeto que establece la conexión con la base de datos.
          Creado previamente a través de la función execute(self)
          ]
    Returns:
        [Boolean]: [
          Retorna True/False y "S/Datos" a través de logger, solo si puede:
            - A
          Retorna True y “Aprobado” a través de logger, solo si se puede: 
            - A
          En todo otro caso, retorna False y "Rechazado" a través de logger.
          ]
    """      
    try:
        rows= conn.execute("""
        select Pi.Identifier,
              (p.FirstName || ' ' || p.MiddleName || ' ' || p.LastName || ' ' || p.SecondLastName) as "nombre completo",
              pdc.DegreeOrCertificateTitleOrSubject,
              pdc.AwardDate,
              pdc.NameOfInstitution,
              rae.RefAttendanceStatusId
                ,
              rae.observaciones
        from Person P
                join OrganizationPersonRole opr on p.PersonId = Opr.PersonId
                join PersonDegreeOrCertificate pdc on p.PersonId = pdc.PersonId
                join RoleAttendanceEvent rae on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId
                join PersonIdentifier pi on pi.PersonId = p.PersonId
        where RoleId != 6
          and rae.observaciones like '%Falta docente%';
                """).fetchall()
        if(len(rows)>0):
            identificador = (list(set([m[0] for m in rows if m[0] is not None])))
            if not identificador:
                logger.error(f"Sin identificador")
                logger.error(f'Rechazado')
                return_dict[getframeinfo(currentframe()).function] = False
                return False
            nombre = (list(set([m[1] for m in rows if m[1] is not None])))
            if not nombre:
                logger.error(f"Sin nombre")
                logger.error(f'Rechazado')
                return_dict[getframeinfo(currentframe()).function] = False
                return False
            titulo = (list(set([m[2] for m in rows if m[2] is not None])))
            if not titulo:
                logger.error(f"Sin titulo")
                logger.error(f'Rechazado')
                return_dict[getframeinfo(currentframe()).function] = False
                return False
            fechatitulo = (list(set([m[3] for m in rows if m[3] is not None])))
            if not fechatitulo:
                logger.error(f"Sin fecha de titulo")
                logger.error(f'Rechazado')
                return_dict[getframeinfo(currentframe()).function] = False
                return False
            institucion = (list(set([m[4] for m in rows if m[4] is not None])))
            if not institucion:
                logger.error(f"Sin institucion")
                logger.error(f'Rechazado')
                return_dict[getframeinfo(currentframe()).function] = False
                return False
            observacion = (list(set([m[5] for m in rows if m[5] is not None])))
            if not observacion:
                logger.error(f"Sin observacion")
                logger.error(f'Rechazado')
                return_dict[getframeinfo(currentframe()).function] = False
                return False
            logger.info(f"Docentes validados")
            logger.info(f"Aprobado")
            return_dict[getframeinfo(currentframe()).function] = True
            return True
        else:
            logger.info(f"S/Datos")
            logger.info(f"No existen clases en las que haya faltado algún docente")
            return_dict[getframeinfo(currentframe()).function] = True
            return True
    except Exception as e:
        logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
        logger.error(f"Rechazado")
        return_dict[getframeinfo(currentframe()).function] = False
        return False
  ## Fin fn5E2 WC ##