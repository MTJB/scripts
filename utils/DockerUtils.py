import os
import platform
import subprocess


def get_sqlcmd_cmdline(db_name='master', sql=None):
    file_name = 'tmp.sql'
    created_file = None
    sqlcmd = f"/opt/mssql-tools/bin/sqlcmd -s '\t' -b -U sa -S 127.0.0.1 -P " \
             f"'sqlP4..w0rd' -d '{db_name}' "

    if sql is not None and len(sql) > 500:
        f = open(file_name, 'x')
        f.write(sql)
        created_file = f.name
        docker_cp('tmp.sql', "mssql:/tmp")
        sqlcmd += "-i /tmp/tmp.sql"
        if os.path.exists(file_name):
            os.remove(file_name)
    elif sql is None:
        sqlcmd += "-Q \"{}\""
    else:
        sqlcmd += f"-Q \"{sql}\""

    return sqlcmd, created_file


def docker_exec_ok(container, cmd, show_log=True, work_dir=None):
    r = docker_exec(container, cmd, show_log=show_log, work_dir=work_dir)
    if r.exit_code != 0:
        raise Exception("sqL_failed" + r.output.decode("utf-8"))
    return r


def docker_exec(container, cmd, work_dir=None, show_log=True):
    r = container.exec_run(cmd, stdout=show_log, workdir=work_dir)
    print(r.output.decode("utf-8"))
    return r


def docker_cp(src, dest):
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        subprocess.Popen(f"docker cp {src} {dest}", shell=True, stdout=subprocess.PIPE).wait()
    else:
        subprocess.Popen(f"docker cp {src} {dest}", stdout=subprocess.PIPE).wait()
