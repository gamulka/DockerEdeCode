from inspect import getframeinfo, currentframe
from multiprocessing import current_process


from ede.ede._logger import logger

def fn2BA(conn, return_dict):
    """ Breve descripción de la función
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
        _query = conn.execute("""
        SELECT DISTINCT P.PersonId
        from OrganizationPersonRole OPR
                join Person P on OPR.PersonId = P.PersonId
                join PersonStatus PS on P.PersonId = PS.PersonId
        where OPR.RoleId = 6
          and PS.RefPersonStatusTypeId IN (25, 24, 31);
        """).fetchall()
        if (len(_query)>0):
          _queryExcedentes = conn.execute("""
          SELECT fileScanBase64
          from PersonStatus
          where PersonId in (
              SELECT DISTINCT P.PersonId
              FROM OrganizationPersonRole OPR
                      join Person P on OPR.PersonId = P.PersonId
                      join PersonStatus PS on P.PersonId = PS.PersonId
              where OPR.RoleId = 6
                and PS.RefPersonStatusTypeId IN (25, 24, 31))
            and fileScanBase64 is not null
            and RefPersonStatusTypeId IN (25, 24, 31);
          """).fetchall()
          if (len(_queryExcedentes) == len(_query)):
            _file = conn.execute("""
            SELECT documentId
            FROM Document
            WHERE fileScanBase64 IS NOT NULL
              AND fileScanBase64 <> ''
              AND documentId in (select fileScanBase64
                                from PersonStatus
                                where PersonId in (
                                    select DISTINCT P.PersonId
                                    from OrganizationPersonRole OPR
                                              join Person P on OPR.PersonId = P.PersonId
                                              join PersonStatus PS on P.PersonId = PS.PersonId
                                    where OPR.RoleId = 6
                                      and PS.RefPersonStatusTypeId IN (25, 24, 31)
                                )
                                  and fileScanBase64 is not null
                                  and RefPersonStatusTypeId IN (25, 24, 31)
            )
            """).fetchall()
            if(len(_file) == len(_query)):
              logger.info(f'Todos los alumnos excedentes cuentan con su documento correspondiente')
              logger.info(f'Aprobado')
              return_dict[getframeinfo(currentframe()).function] = True
              return True
            else:
              logger.error(f'Los alumnos excedentes no cuentan con su documento correspondiente')
              logger.error(f'Rechazado')
              return_dict[getframeinfo(currentframe()).function] = False
              return False
          else:
            logger.error(f'Los alumnos excedentes no cuentan con su documento correspondiente')
            logger.error(f'Rechazado')
            return_dict[getframeinfo(currentframe()).function] = False
            return False
        else:
            logger.info(f'S/Datos')
            logger.info(f'No existen alumnos excedentes en el establecimiento')
            return_dict[getframeinfo(currentframe()).function] = True
            return True
    except Exception as e:
        logger.error(f'NO se pudo ejecutar la verificación en la lista')
        logger.error(f'Rechazado')
        return_dict[getframeinfo(currentframe()).function] = False
        return False
  ## Fin fn2BA WC ##