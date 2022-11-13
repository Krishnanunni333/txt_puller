import click


def display_error(content):
    click.secho("ERROR: {}".format(content), fg="red", bold=True)

def display_success(content):
    click.secho("SUCCESS: {}".format(content), fg="green", bold=True)

def display_warning(content):
    click.secho("WARNING: {}".format(content), fg="yellow", bold=True)

def display_files(content):
    click.secho("----------ALL FILES---------\n{}".format(content), fg="blue", bold=True)