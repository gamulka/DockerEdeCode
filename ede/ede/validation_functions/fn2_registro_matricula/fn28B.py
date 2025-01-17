from inspect import getframeinfo, currentframe
from multiprocessing import current_process


from ede.ede._logger import logger

def fn28B(conn, return_dict):
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
        SELECT DISTINCT PI.PersonId
        FROM OrganizationPersonRole OPR
                join Person P on OPR.PersonId = P.PersonId
                join PersonIdentifier PI on P.PersonId = PI.PersonId
        WHERE PI.RefPersonIdentificationSystemId = 52
          AND OPR.RoleId = 6
          AND PI.Identifier is not null;
        """).fetchall()
        if(len(_query)>0):
          _queryDocuments = conn.execute("""
          SELECT PS.fileScanBase64
          FROM PersonStatus PS
          WHERE PS.PersonId in (select DISTINCT PI.PersonId
                                from OrganizationPersonRole OPR
                                        join Person P on OPR.PersonId = P.PersonId
                                        join PersonIdentifier PI on P.PersonId = PI.PersonId
                                where PI.RefPersonIdentificationSystemId = 52
                                  and OPR.RoleId = 6
                                  and PI.Identifier is not null)
            AND PS.docNumber IS NOT NULL
            AND PS.docNumber <> ''
            AND PS.Description IS NOT NULL
            AND PS.Description <> ''
            and PS.fileScanBase64 is not null
            and PS.RefPersonStatusTypeId = 34
          """).fetchall()
          if (len(_queryDocuments) == len(_query)):
            _file = conn.execute("""
            SELECT documentId
            FROM Document
            WHERE fileScanBase64 IS NOT NULL
              AND fileScanBase64 <> ''
              AND documentId in (SELECT PS.fileScanBase64
                                FROM PersonStatus PS
                                WHERE PS.PersonId in (select DISTINCT PI.PersonId
                                                      from OrganizationPersonRole OPR
                                                                join Person P on OPR.PersonId = P.PersonId
                                                                join PersonIdentifier PI on P.PersonId = PI.PersonId
                                                      where PI.RefPersonIdentificationSystemId = 52
                                                        and OPR.RoleId = 6
                                                        and PI.Identifier is not null)
                                  AND PS.docNumber IS NOT NULL
                                  AND PS.docNumber <> ''
                                  AND PS.Description IS NOT NULL
                                  AND PS.Description <> ''
                                  and PS.fileScanBase64 is not null
                                  and PS.RefPersonStatusTypeId = 34);
            """).fetchall()
            if(len(_file) == len(_query)):
              logger.info(f'Todos los estudiantes migrantes cuentan con sus documentos de convalidacion de ramos completos')
              logger.info(f'Aprobado')
              return_dict[getframeinfo(currentframe()).function] = True
              return True
            else:
              logger.error(f'Existen alumnos migrantes con documentos de convalidacion de ramos incompletos')
              logger.error(f'Rechazado')
              return_dict[getframeinfo(currentframe()).function] = False
              return False
          else:
            logger.error(f'Existen alumnos migrantes con documentos de convalidacion de ramos incompletos')
            logger.error(f'Rechazado')
            return_dict[getframeinfo(currentframe()).function] = False
            return False
        else:
            logger.info(f"No existen estudiantes migrantes registrados en el establecimiento")
            logger.info(f"S/Datos")
            return_dict[getframeinfo(currentframe()).function] = True
            return True
    except Exception as e:
        logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
        logger.error(f"Rechazado")
        return_dict[getframeinfo(currentframe()).function] = False
        return False
  ## Fin fn28B WC ##