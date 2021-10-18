import docker

from utils import DockerUtils


def exec_sql_ok(sql_image, sql, db_name='master', show_log=True):
    docker_cl = docker.from_env()
    sqlcmd, file_name = DockerUtils.get_sqlcmd_cmdline(db_name, sql)
    sql_container = docker_cl.containers.get(sql_image)
    DockerUtils.docker_exec_ok(sql_container, sqlcmd, show_log=show_log)
    DockerUtils.docker_exec_ok(sql_container, f"rm /tmp/{file_name}", show_log=False)  # Clean up file (if there)
