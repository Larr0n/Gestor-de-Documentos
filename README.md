# Gestor-de-Documentos
Basado en la necesidad real de un oficina que necesitaba registrar los movimientos de legajos y documentos que llevaba a cabo, desarrollé este proyecto para tratar de que su trabajo fuera más fácil.
Con este sistema, se mejora significativamente la trazabilidad de los documentos físicos que gestionan cotidianamente, como expedientes de retiro, cómputos de servicios, resoluciones y otros. El objetivo principal es brindar una herramienta intuitiva, confiable y escalable que mejore la administración de estos documentos.
Con las funciones desarrolladas y la interfaz gráfica, el usuario puede:
1) Ingresar mediante un login, para mantener la seguridad e integridad de los datos
2) Consultar datos con filtros dinámicos por DNI, apellido, nombre, legajo, grado y tipo de documento.
3) Insertar y eliminar registros de forma controlada.
4) Editar celdas directamente desde la grilla.
5) Exportar consultas personalizadas a excel.
Se guarda toda la actividad de los usuarios en un archivo de logs, por si se quiere indagar el comportamiento de uno en particular.
Además, cuenta con un backup automático (cada vez que se realiza un login), así en caso de borrar datos sin querer, se pueden recuperar de manera simple.
