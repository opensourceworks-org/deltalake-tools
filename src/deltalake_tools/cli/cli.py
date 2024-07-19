import click
import logging

from deltalake_tools.core.core import (
    delta_compact,
    delta_vacuum,
    delta_create_checkpoint,
    table_version as delta_table_version
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.1')
def cli():
    pass


@cli.command()
@click.argument('delta-table-path')
def compact(delta_table_path: str):
    result = delta_compact(delta_table_path)

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())


@cli.command()
@click.argument('delta-table-path')
@click.option('--retention-hours', default=168, type=int)
@click.option('--disable-retention-duration', is_flag=True)
@click.option('--force', is_flag=True)
def vacuum(delta_table_path: str,
        retention_hours: int,
        disable_retention_duration: bool = False,
        force: bool = False):

    result = delta_vacuum(
                delta_table_path,
                retention_hours=retention_hours,
                enforce_retention_duration=not disable_retention_duration,
                dry_run=not force,
    )

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())

@cli.command()
@click.argument('delta-table-path')
def create_checkpoint(delta_table_path: str):
    result = delta_create_checkpoint(delta_table_path)

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())

@cli.command()
@click.argument('delta-table-path')
def table_version(delta_table_path: str):
    result = delta_table_version(delta_table_path)

    if result.is_err():
        print(result.unwrap_err())
    else:
        print(result.unwrap())
