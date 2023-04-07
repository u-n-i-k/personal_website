import argparse
import logging

from personal_website.alembic.migrations import AlembicHelper
from personal_website.application import App
from personal_website.core.config import Config
from personal_website.core.utils import ArgEnum
from personal_website.pycron_jobs import pycron_jobs

log = logging.getLogger("personal_website")


class Job(ArgEnum):
    webapp = "webapp"
    alembic = "alembic"
    pycron = "pycron"


class AlembicCmd(ArgEnum):
    create_migration = "create_migration"
    set_revision = "set_revision"
    show_diff = "show_diff"


def main() -> None:
    prog = "python -m personal_website"
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument(
        "-c",
        "--config",
        dest="config_path",
        metavar="config_path",
        default="config.json",
        type=str,
    )
    parser.add_argument(
        "-j",
        "--job",
        dest="job_name",
        choices=list(Job),
        type=lambda val: Job[val],
        default=Job.webapp,
    )
    parser.add_argument(
        "-a",
        "--job-args",
        dest="job_args",
        metavar="job_arg",
        nargs="*",
    )
    args = parser.parse_args()

    config = Config.parse_file(args.config_path)

    if args.job_name == Job.webapp:
        AlembicHelper(
            config.db_conn.sqlalchemy_async_database_uri,
            config.db_conn.dbschema,
        ).upgrade_to_revision("head")
        App(config).run()
    elif args.job_name == Job.alembic:
        alembic_helper = AlembicHelper(
            config.db_conn.sqlalchemy_async_database_uri,
            config.db_conn.dbschema,
        )
        alembic_parser = argparse.ArgumentParser(
            prog=f"{prog} --job alembic --job-args"
        )
        alembic_parser.add_argument(
            "command",
            choices=list(AlembicCmd),
            type=lambda val: AlembicCmd[val],
        )
        alembic_parser.add_argument("arg", type=str)
        alembic_args = alembic_parser.parse_args(args.job_args)

        if alembic_args.command == AlembicCmd.create_migration:
            message = alembic_args.arg
            alembic_helper.create_migration(message)
        elif alembic_args.command == AlembicCmd.set_revision:
            alembic_helper.downgrade_to_revision("base")
            alembic_helper.upgrade_to_revision(alembic_args.arg)
        elif alembic_args.command == AlembicCmd.show_diff:
            sql = alembic_helper.upgrade_to_revision(alembic_args.arg, sql=True)
            log.info(sql)
    elif args.job_name == Job.pycron:
        pycron_parser = argparse.ArgumentParser(prog=f"{prog} --job pycron --job-args")
        pycron_parser.add_argument("crontab", type=str)
        pycron_parser.add_argument("job", choices=pycron_jobs.keys())
        pycron_args = pycron_parser.parse_args(args.job_args)
        log.info("Running %s with schedule '%s'", pycron_args.job, pycron_args.crontab)
        pycron_jobs[pycron_args.job](pycron_args.crontab).run()


if __name__ == "__main__":
    main()
