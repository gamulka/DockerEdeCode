from inspect import getframeinfo, currentframe
from multiprocessing import current_process

from ede.ede._logger import logger
### INICIO fn3F2 ###
def fn3F2(conn, return_dict):
    """
    Integridad: Verifica que lista personList contenga información
    Args:
        conn ([sqlalchemy.engine.Connection]): [
          Objeto que establece la conexión con la base de datos.
          Creado previamente a través de la función execute(self)
          ]
    Returns:
        [Boolean]: [
          Retorna True y “Aprobado” a través de logger, solo si se puede: 
            - encontrar la información mínima solicitada en la BD
          En todo otro caso, retorna False y "Rechazado" a través de logger.
          ]
    """ 
    _r = False
    rows = []
    try:
      rows = conn.execute("""
        SELECT
          RUN
        FROM PersonList;
      """).fetchall()
    except Exception as e:
      logger.info(f"Resultado: {rows} -> {str(e)}")
    try:
      if(len(rows)>0):
        logger.info(f"len(personList): {len(rows)}")
        logger.info(f"Aprobado")
        _r = True        
      else:
        logger.info(f"S/Datos")
    except Exception as e:
      logger.error(f"No se pudo ejecutar la consulta a la vista personList: {str(e)}")
      logger.error(f"Rechazado")
    finally:
      return_dict[getframeinfo(currentframe()).function] = _r
      logger.info(f"{current_process().name} finalizando...")      
      return _r
  ### FIN fn3F2 ###